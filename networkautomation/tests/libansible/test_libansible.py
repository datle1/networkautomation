from unittest import TestCase
from networkautomation.drivers.ansible.libansible import *

test_ansible_config_file = ".ansible.cfg"

class LibansibileTest(TestCase):

    def test_create_ansible_cfg(self):
        create_ansible_cfg()
        import napalm_ansible
        import ntc_ansible_plugin
        napalm_module_dir = "{}".format(os.path.dirname(
            napalm_ansible.__file__))
        ntc_ansible_dir = "{}".format(os.path.dirname(
            ntc_ansible_plugin.__file__))
        file_path = os.environ['HOME'] + "/" + test_ansible_config_file
        with open(file_path, "r") as file:
            content = file.read()
        os.remove(file_path)
        expect = '[defaults]\n' \
                'host_key_checking=False\n' \
                'log_path=/var/log/ansible.log\n' \
                'ansible_python_interpreter=\"/usr/bin/env python\"\n' \
                'action_plugins={}/plugins/action\n' \
                'library={}/modules:{}\n' \
                .format(napalm_module_dir, napalm_module_dir, ntc_ansible_dir)
        self.assertEqual(content, expect)
