from enum import Enum

from ansible import context
from ansible.errors import AnsibleError
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager


INVENTORY_FILE = "/tmp/inventory"

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
        h1 = '{0} ansible_ssh_user={1} ansible_ssh_pass={2}\n'\
            .format(host, username, password)
        f.write(h1)


def execute_playbook(playbook, host, user, password, variables):
    loader = DataLoader()
    context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False,
                                    listhosts=False, syntax=False,
                                    connection='ssh',
                                    module_path=None, forks=1,
                                    remote_user=user, private_key_file=None,
                                    ssh_common_args=None, ssh_extra_args=None,
                                    sftp_extra_args=None, scp_extra_args=None,
                                    become=True, run_one=True,
                                    become_method='sudo', become_user='root',
                                    verbosity=True, check=False, serial=1,
                                    start_at_task=None)
    create_inventory(INVENTORY_FILE, host, user, password, 'all')
    inventory = InventoryManager(loader=loader, sources=INVENTORY_FILE)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    if variables:
        variable_manager.extra_vars.update(variables)
    executor = PlaybookExecutor(playbooks=[playbook],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                passwords={'conn_pass': password})
    try:
        results = executor.run()
        msg = PlaybookResult(results)
        if msg == PlaybookResult.RUN_OK:
            return True, None
        else:
            return False, msg
    except AnsibleError as err:
        print(err.message)
        executor._tqm.cleanup()
        loader.cleanup_all_tmp_files()
        return False, err.message

