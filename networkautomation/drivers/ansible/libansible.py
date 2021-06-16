import os
from enum import Enum

import napalm_ansible
from ansible import context
from ansible.errors import AnsibleError
from ansible.module_utils.common.collections import ImmutableDict
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager

INVENTORY_FILE = "inventory"
ANSIBLE_CONFIG_FILE = "ansible.cfg"


class PlaybookResult(Enum):
    RUN_OK = 0
    RUN_ERROR = 1
    RUN_FAILED_HOSTS = 2
    RUN_UNREACHABLE_HOSTS = 4
    RUN_FAILED_BREAK_PLAY = 8
    RUN_UNKNOWN_ERROR = 255


def create_ansible_cfg(ansible_conf_file):
    if not os.path.exists(ansible_conf_file):
        napalm_module_dir = "{}".format(os.path.dirname(
            napalm_ansible.__file__))
        with open(ansible_conf_file, 'w') as f:
            f.write('[defaults]\n'
                    'host_key_checking=False\n'
                    'log_path=/var/log/ansible.log\n'
                    'ansible_python_interpreter=\"/usr/bin/env python\"\n'
                    'action_plugins={}/plugins/action\n'
                    'library={}/modules\n'
                    .format(napalm_module_dir, napalm_module_dir))


def create_inventory(inventory_path, host, username, password, group):
    with open(inventory_path, 'w') as f:
        f.write('[{}]\n'.format(group))
        h1 = '{0} ansible_ssh_user={1} ansible_ssh_pass={2} ' \
             'ansible_python_interpreter="/usr/bin/env python"\n' \
            .format(host, username, password)
        f.write(h1)


def execute_playbook(playbook, host, user, password, extra_vars):
    loader = DataLoader()
    context.CLIARGS = ImmutableDict(tags={}, listtags=False, listtasks=False,
                                    listhosts=False, syntax=False,
                                    module_path=None, verbosity=True,
                                    check=False, start_at_task=None,
                                    forks=1)
    create_ansible_cfg(ANSIBLE_CONFIG_FILE)
    create_inventory(INVENTORY_FILE, host, user, password, 'all')
    inventory = InventoryManager(loader=loader, sources=INVENTORY_FILE)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    if extra_vars:
        variable_manager.extra_vars.update(extra_vars)

    executor = PlaybookExecutor(playbooks=[playbook],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                passwords=None)
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
