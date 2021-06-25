import os
from unittest import TestCase
from unittest.mock import MagicMock
from networkautomation.drivers.ansible import libansible

file_path = "ansible.cfg"

class LibansibileTest(TestCase):

    def test_create_ansible_cfg(self):
        libansible.install_collection = MagicMock(name='install_collection')
        libansible.download_generate_ansible_cfg(file_path)
        import napalm_ansible
        import ntc_ansible_plugin
        napalm_module_dir = "{}".format(os.path.dirname(
            napalm_ansible.__file__))
        ntc_ansible_dir = "{}".format(os.path.dirname(
            ntc_ansible_plugin.__file__))
        with open(file_path, "r") as file:
            content = file.read()
        os.remove(file_path)
        a10_acos_axapi_path = os.environ['HOME'] + \
                              '/collections/ansible_collections'
        expect = '[defaults]\n' \
                'host_key_checking=False\n' \
                'log_path=/var/log/ansible.log\n' \
                'ansible_python_interpreter=\"/usr/bin/env python\"\n' \
                'action_plugins={}/plugins/action\n' \
                'library={}/modules:{}\n' \
                'collections_paths={}\n' \
                .format(napalm_module_dir,
                        napalm_module_dir,
                        ntc_ansible_dir,
                        a10_acos_axapi_path)
        self.assertEqual(content, expect)
