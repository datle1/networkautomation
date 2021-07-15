from enum import Enum
from ansible import context
from ansible.errors import AnsibleError
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.plugins.callback.default import CallbackModule
from ansible.vars.manager import VariableManager
from networkautomation.drivers.ansible import ansible_utils


class PlayBookResultsCollector(CallbackModule):
    CALLBACK_VERSION = 2.0

    def __init__(self):
        super(PlayBookResultsCollector, self).__init__()
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}
        self.status_no_hosts = False
        self.display_skipped_hosts = True
        self.display_ok_hosts = True
        self._plugin_options = {'show_per_host_start': False}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        self.task_skipped[result._host.get_name()] = result

    def v2_playbook_on_no_hosts_matched(self):
        self.status_no_hosts = True

    def v2_playbook_on_stats(self, stats):

        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "success": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }

    def getPlaybookResult(self):
        if self.status_no_hosts:
            results = {'msg': "Could not match supplied host pattern",
                       'flag': False, 'executed': False}
            return results
        results_info = {'skipped': {}, 'failed': {}, 'success': {},
                        "status": {}, 'unreachable': {}, "changed": {}}
        for host, result in self.task_ok.items():
            results_info['success'][host] = result._result
        for host, result in self.task_failed.items():
            results_info['failed'][host] = result
        for host, result in self.task_status.items():
            results_info['status'][host] = result
        for host, result in self.task_skipped.items():
            results_info['skipped'][host] = result
        for host, result in self.task_unreachable.items():
            results_info['unreachable'][host] = result
        return results_info


class PlaybookResult(Enum):
    RUN_OK = 0
    RUN_ERROR = 1
    RUN_FAILED_HOSTS = 2
    RUN_UNREACHABLE_HOSTS = 4
    RUN_FAILED_BREAK_PLAY = 8
    RUN_UNKNOWN_ERROR = 255


def execute_playbook(playbook, host, config, input_vars=None, tags=None):
    ansible_utils.create_inventory(host, config, 'all',
                                   ansible_utils.INVENTORY_FILE)
    loader = DataLoader()
    tags = tags or []
    context.CLIARGS = ImmutableDict(tags=tags, listtags=False, listtasks=False,
                                    listhosts=False, syntax=False,
                                    module_path=None, verbosity=True,
                                    check=False, start_at_task=None,
                                    forks=1)
    inventory = InventoryManager(loader=loader,
                                 sources=ansible_utils.INVENTORY_FILE)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    if input_vars:
        variable_manager.extra_vars.update(input_vars)

    executor = PlaybookExecutor(playbooks=[playbook],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                passwords=None)
    try:
        results_callback = PlayBookResultsCollector()
        executor._tqm._stdout_callback = results_callback
        results = executor.run()
        playbook_result = results_callback.getPlaybookResult()
        msg = PlaybookResult(results)
        if msg == PlaybookResult.RUN_OK:
            return True, None
        elif msg == PlaybookResult.RUN_FAILED_HOSTS:
            failed_result = 'Error: ' + \
                            str(playbook_result["failed"][host]._result)
            failed_task = 'Ansible task: ' + \
                          str(playbook_result["failed"][host].task_name)
            return False, failed_task + '. ' + failed_result
        else:
            return False, msg
    except AnsibleError as err:
        print(err.message)
        executor._tqm.cleanup()
        loader.cleanup_all_tmp_files()
        return False, err.message
    finally:
        ansible_utils.delete_inventory(ansible_utils.INVENTORY_FILE)
