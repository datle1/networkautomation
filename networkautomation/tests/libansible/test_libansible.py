import os
from unittest import TestCase
from unittest.mock import MagicMock
from networkautomation.drivers.ansible import ansible_utils

ansible_cfg_path = "ansible.cfg"
inventory_path = "inventory"


class LibansibileTest(TestCase):

    def test_create_ansible_cfg(self):
        ansible_utils.install_collection = MagicMock(name='install_collection')
        ansible_utils.download_generate_ansible_cfg(ansible_cfg_path)
        import napalm_ansible
        import ntc_ansible_plugin
        napalm_module_dir = "{}".format(os.path.dirname(
            napalm_ansible.__file__))
        ntc_ansible_dir = "{}".format(os.path.dirname(
            ntc_ansible_plugin.__file__))
        with open(ansible_cfg_path, "r") as file:
            content = file.read()
        os.remove(ansible_cfg_path)
        a10_acos_axapi_path = os.environ['HOME'] + '/.ansible/collections'
        expect = '[defaults]\n' \
                 'host_key_checking=False\n' \
                 'log_path=/var/log/ansible.log\n' \
                 'ansible_python_interpreter=\"/usr/bin/env python\"\n' \
                 'action_plugins={}/plugins/action:{}\n' \
                 'library={}/modules:{}:{}\n' \
            .format(napalm_module_dir,
                    a10_acos_axapi_path +
                    '/ansible_collections/a10/acos_axapi/plugins/action',
                    napalm_module_dir,
                    ntc_ansible_dir,
                    a10_acos_axapi_path +
                    '/ansible_collections/a10/acos_axapi/plugins/modules',
                    a10_acos_axapi_path)
        self.assertEqual(content, expect)

    def test_create_inventory_user_pass(self):
        ansible_utils.create_inventory('localhost',
                                       {'ansible_ssh_user': 'admin',
                                        'ansible_ssh_pass': 'admin'},
                                       'all', inventory_path)
        with open(inventory_path, "r") as file:
            content = file.read()
        os.remove(inventory_path)
        expect = '[all]\nlocalhost ansible_python_interpreter="/usr/bin/env ' \
                 'python" ansible_ssh_user=admin ansible_ssh_pass=admin '
        self.assertEqual(content, expect)

    def test_create_inventory_vim_url(self):
        ansible_utils.create_inventory('localhost', {'vim_url': 'abc'}, 'all',
                                       inventory_path)
        with open(inventory_path, "r") as file:
            content = file.read()
        os.remove(inventory_path)
        expect = '[all]\nlocalhost ansible_python_interpreter="/usr/bin/env ' \
                 'python" vim_url=abc '
        self.assertEqual(content, expect)
