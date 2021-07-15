import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock
from networkautomation.drivers.ansible import ansible_utils, libansible

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
                 'log_path=/tmp/ansible.log\n' \
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
                                        'ansible_ssh_pass': 'admin',
                                        'vim_url': 'abc'},
                                       'all', inventory_path)
        with open(inventory_path, "r") as file:
            content = file.read()
        os.remove(inventory_path)
        expect = '[all]\nlocalhost ansible_python_interpreter="/usr/bin/env ' \
                 'python3" ansible_ssh_user=admin ansible_ssh_pass=admin ' \
                 'vim_url=abc '
        self.assertEqual(content, expect)

    def test_run_playbook(self):
        loadbalancer_model = {'load_balancer': {'name': 'vLB'}}
        playbook = '---\n' \
                   '- name: Test job apply\n' \
                   '  gather_facts: false\n' \
                   '  hosts: all\n' \
                   '  connection: local\n' \
                   '  tasks:\n' \
                   '    - name: Touch a file "{{ load_balancer.name }}"\n' \
                   '      file:\n' \
                   '        path: "{{ load_balancer.name }}"\n' \
                   '        state: touch\n' \
                   '    - name: Verify\n' \
                   '      shell: "ls -l {{ load_balancer.name }}"\n' \
                   '      register: playbook_path_output\n' \
                   '    - debug: var=playbook_path_output.stdout\n' \
                   '    - name: Remove file (delete file)\n' \
                   '      file:\n' \
                   '        path: "{{ load_balancer.name }}"\n' \
                   '        state: absent'
        file = 'try.yaml'
        with open(file, 'w') as f:
            f.write(playbook)
        res, error = libansible.execute_playbook(file,
                                                 '127.0.0.1',
                                                 None,
                                                 input_vars=loadbalancer_model)
        os.remove(file)
        self.assertEqual((True, None), (res, error))
