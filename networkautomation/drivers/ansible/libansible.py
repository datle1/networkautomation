import os
from enum import Enum
from ansible import context
from ansible.errors import AnsibleError
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.plugins.callback import CallbackBase


INVENTORY_FILE = "inventory"
ANSIBLE_CONFIG_FILE = ".ansible.cfg"

def create_ansible_cfg():
    file_path = os.environ['HOME'] + "/" + ANSIBLE_CONFIG_FILE
    if not os.path.exists(file_path):
        import napalm_ansible
        import ntc_ansible_plugin
        napalm_module_dir = "{}".format(os.path.dirname(
            napalm_ansible.__file__))
        ntc_ansible_dir = "{}".format(os.path.dirname(
            ntc_ansible_plugin.__file__))
        with open(file_path, 'w') as f:
            f.write('[defaults]\n'
                    'host_key_checking=False\n'
                    'log_path=/var/log/ansible.log\n'
                    'ansible_python_interpreter=\"/usr/bin/env python\"\n'
                    'action_plugins={}/plugins/action\n'
                    'library={}/modules:{}\n'
                    .format(napalm_module_dir, napalm_module_dir,
                            ntc_ansible_dir))


class PlayBookResultsCollector(CallbackBase):
    CALLBACK_VERSION = 2.0

    def __init__(self, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}
        self.status_no_hosts = False

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
            results = {'msg': "Could not match supplied host pattern", 'flag': False, 'executed': False}
            return results
        results_info = {'skipped': {}, 'failed': {}, 'success': {}, "status": {}, 'unreachable': {}, "changed": {}}
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


def create_inventory(inventory_path, host, username, password, group):
    with open(inventory_path, 'w') as f:
        f.write('[{}]\n'.format(group))
        h1 = '{0} ansible_ssh_user={1} ansible_ssh_pass={2} ' \
             'ansible_python_interpreter="/usr/bin/env python"\n' \
            .format(host, username, password)
        f.write(h1)


def delete_inventory(inventory_path):
    if os.path.exists(inventory_path):
        os.remove(inventory_path)


def execute_playbook(playbook, host, user, password, input_vars):
    create_inventory(INVENTORY_FILE, host, user, password, 'all')
    loader = DataLoader()
    context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False,
                                    listhosts=False, syntax=False,
                                    module_path=None, verbosity=True,
                                    check=False, start_at_task=None,
                                    forks=1)
    inventory = InventoryManager(loader=loader, sources=INVENTORY_FILE)
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
            reasons = []
            failed_result = playbook_result["failed"][host]._result
            if failed_result.get("results") is not None:
                # when multi tasks failed
                task_results = playbook_result["failed"][host]._result.get("results")
                for task_result in task_results:
                    reasons.append(task_result["msg"])
                return False, reasons
            else:
                # When only one task failed
                reasons.append(failed_result["msg"])
                return False, reasons
        else:
            return False, msg
    except AnsibleError as err:
        print(err.message)
        executor._tqm.cleanup()
        loader.cleanup_all_tmp_files()
        return False, err.message
    finally:
        delete_inventory(INVENTORY_FILE)
