from unittest import TestCase, mock
from networkautomation import common, network_function
from networkautomation.drivers.driver_factory import DriverFactory
from networkautomation.job_manager import *


class FunctionalTest(TestCase):
    vlan_model = {'vlan_config': {'vlan_id': 123}}
    loadbalancer_model = {'load_balancer': {'name': 'vLB'}}
    target_octavia = network_function.NetworkFunction(
        'loadbalancer',
        'octavia',
        'amphora',
        '2.0',
        '127.0.0.1',
        other_auth_info={
            'auth_url': 'localhost:5000/v3',
            'username': 'admin',
            'password': 'admin',
            'project_name': 'admin',
            'user_domain_name': 'Default',
            'project_domain_name': 'Default'
        })
    target_a10 = network_function.NetworkFunction(
        'loadbalancer',
        'a10',
        'acos',
        '2.0',
        '127.0.0.1',
        other_auth_info={
            'ansible_username': 'admin',
            'ansible_password': 'admin',
            'ansible_port': 443
        })
    target_common = network_function.NetworkFunction(
        'switch',
        'arista',
        'eos',
        '4.1',
        '127.0.0.1',
        ssh_user='admin',
        ssh_pass='admin')

    def test_execute_ansible_job(self):
        data_model = self.loadbalancer_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=180,
            apply_template='playbooks/apply.yaml')
        self.assertEqual((True, None), (result, error))

    def test_execute_rest_job(self):
        target = self.target_common
        data_model = self.vlan_model
        result, error = JobManager().execute_job(
            target, data_model, action=common.ActionType.CREATE,
            element='vlan_config')
        self.assertEqual((False, '[Task INIT - Driver is not found]'),
                         (result, error))

    def test_execute_ansible_job_timeout_backup(self):
        data_model = self.vlan_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            backup_template='playbooks/timeout.yaml')
        self.assertEqual((False, '[Task BACKUP - Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_apply(self):
        data_model = self.vlan_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            apply_template='playbooks/timeout.yaml')
        self.assertEqual((False, '[Task APPLY - Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_verify(self):
        data_model = self.vlan_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            verify_template='playbooks/timeout.yaml')
        self.assertEqual((False, '[Task VERIFY - Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_rollback(self):
        data_model = self.vlan_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            apply_template='playbooks/timeout.yaml',
            rollback_template='playbooks/timeout.yaml')
        self.assertEqual((False, '[Task APPLY - Timeout after 1 seconds, '
                                 'Task ROLLBACK - Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_napalm(self):
        data_model = self.vlan_model
        target = self.target_common
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/napalm.yaml')
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_ntc(self):
        data_model = self.vlan_model
        target = self.target_common
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/ntc.yaml')
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_job_module_failed(self):
        data_model = self.loadbalancer_model
        target = self.target_octavia
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/error_open_file.yaml')
        err = "[Task APPLY - Ansible task: Read file. Error: {'msg': 'could " \
              "not locate file in lookup: vLB', '_ansible_no_log': None}]"
        self.assertEqual((False, err), (result, error))

    @mock.patch.object(DriverFactory, 'get_driver_dir')
    def test_execute_a10_create_lb(self, mock_method):
        mock_method.return_value = '../drivers/ansible/'
        data_model = self.loadbalancer_model
        target = self.target_a10
        result, error = JobManager().execute_job(
            target, data_model, action=common.ActionType.CREATE,
            element='loadbalancer')
        self.assertEqual((False, '[Task APPLY - Ansible task: include_role : '
                                 'pool. Error: {\'msg\': "\'loadbalancer\' is '
                                 'undefined", \'_ansible_no_log\': False}]'),
                         (result, error))

    @mock.patch.object(DriverFactory, 'get_driver_dir')
    def test_execute_ansible_vlb_octavia(self, mock_method):
        mock_method.return_value = '../drivers/ansible/'
        data_model = self.loadbalancer_model
        target = self.target_octavia
        result, error = JobManager().execute_job(
            target, data_model, action=common.ActionType.CREATE,
            element='loadbalancer')
        self.assertEqual((False,
                          '[Task APPLY - Ansible task: Create a vLB '
                          'Openstack. Error: {\'msg\': "The task includes an '
                          'option with an undefined '
                          "variable. The error was: 'loadbalancer' is undefined\\n\\nThe error appears "
                          'to be in '
                          "'/home/nito/git/networkautomation/networkautomation/drivers/ansible/templates/loadbalancer/octavia/amphora/roles/loadbalancer/tasks/create.yaml': "
                          'line 2, column 3, but may\\nbe elsewhere in the file depending on the exact '
                          'syntax problem.\\n\\nThe offending line appears to be:\\n\\n---\\n- name: '
                          'Create a vLB Openstack\\n  ^ here\\n", \'_ansible_no_log\': False}]'),
                         (result, error))
