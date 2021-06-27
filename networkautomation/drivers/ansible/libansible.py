import os
import urllib.request
import zipfile
from enum import Enum
from pathlib import Path

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


def download_package(dir, url):
    file_name = 'temp.zip'
    urllib.request.urlretrieve(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(dir)
    os.remove(file_name)


def install_collection(collections_dir, module_name, download_url,
                       unzip_package):
    dir_list = module_name.split('.')
    a10_collection_path = collections_dir
    for dir in dir_list:
        a10_collection_path += '/' + dir
    if not os.path.exists(a10_collection_path):
        dir_tmp = a10_collection_path.replace(dir_list[len(dir_list) - 1], '')
        Path(dir_tmp).mkdir(parents=True, exist_ok=True)
        download_package(dir_tmp, download_url)
        os.rename(dir_tmp + '/' + unzip_package, a10_collection_path)


def download_generate_ansible_cfg(config_file=None):
    home_dir = os.environ['HOME']
    if config_file:
        file_path = config_file
    else:
        file_path = home_dir + "/" + ANSIBLE_CONFIG_FILE
    import napalm_ansible
    napalm_module_dir = "{}".format(os.path.dirname(
        napalm_ansible.__file__))
    plugin_paths = napalm_module_dir + '/plugins/action'
    module_paths = napalm_module_dir + '/modules'

    import ntc_ansible_plugin
    module_paths += ':' + os.path.dirname(ntc_ansible_plugin.__file__)

    collections_dir = home_dir + '/collections/ansible_collections'
    install_collection(collections_dir, 'a10.acos_axapi',
        'https://codeload.github.com/a10networks/a10-acos-axapi/zip/refs/heads'
        '/master',
        'a10-acos-axapi-master')

    with open(file_path, 'w') as f:
        f.write('[defaults]\n'
                'host_key_checking=False\n'
                'log_path=/var/log/ansible.log\n'
                'ansible_python_interpreter=\"/usr/bin/env python\"\n'
                'action_plugins={}\n'
                'library={}\n'
                'collections_paths={}\n'
                .format(plugin_paths, module_paths, collections_dir))


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


def create_inventory(inventory_path, host, username, password, extra_config,
                     group):
    h1 = host + ' ansible_python_interpreter="/usr/bin/env python" '
    if username and password:
        h1 += 'ansible_ssh_user={1} ansible_ssh_pass={2} '\
            .format(host, username, password)
    if extra_config:
        h1 += extra_config
    with open(inventory_path, 'w') as f:
        f.write('[{}]\n'.format(group))
        f.write(h1)


def delete_inventory(inventory_path):
    if os.path.exists(inventory_path):
        os.remove(inventory_path)


def execute_playbook(playbook, host, user, password, extra_config=None,
                     input_vars=None, tag=None):
    create_inventory(INVENTORY_FILE, host, user, password, extra_config, 'all')
    loader = DataLoader()
    tags = []
    if tag:
        tags.append(tag)
    context.CLIARGS = ImmutableDict(tags=tags, listtags=False, listtasks=False,
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
                reasons.append(failed_result.get("msg") or
                               failed_result.get("reason"))
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
