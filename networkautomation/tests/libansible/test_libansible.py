import os
from unittest import TestCase

from networkautomation.drivers.ansible.libansible import *

test_ansible_config_file = "ansible.cfg"

class LibansibileTest(TestCase):

    def test_create_ansible_cfg(self):
        create_ansible_cfg(test_ansible_config_file)
        napalm_module_dir = "{}".format(os.path.dirname(napalm_ansible.__file__))
        with open(test_ansible_config_file, "r") as file:
            content = file.read()
        os.remove(test_ansible_config_file)
        expect = '[defaults]\n'\
                 'host_key_checking=False\n'\
                 'log_path=/var/log/ansible.log\n'\
                 'ansible_python_interpreter="/usr/bin/env python"\n'\
                 'action_plugins={}/plugins/action\n' \
                 'library={}/modules\n' \
                 .format(napalm_module_dir, napalm_module_dir)
        self.assertEqual(content, expect)
