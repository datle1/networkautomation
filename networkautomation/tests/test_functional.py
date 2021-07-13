from unittest import TestCase, mock
from networkautomation import common, network_function
from networkautomation.drivers.driver_factory import DriverFactory
from networkautomation.job_manager import *


class FunctionalTest(TestCase):
    data_model_1 = {'vlan_config': {'vlan_id': 123}}
    target_1 = network_function.NetworkFunction('vloadbalancer',
                                                'openstack',
                                                'octavia',
                                                '2.0',
                                                '127.0.0.1',
                                                ssh_user='admin',
                                                ssh_pass='password')

    def test_execute_ansible_job(self):
        data_model = {'load_balancer': {'name': 'vLB'}}
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=180,
            apply_template='playbooks/apply.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))

    def test_execute_rest_job(self):
        target = network_function.NetworkFunction('firewall',
                                                  'fortinet',
                                                  'fortios',
                                                  '7.1',
                                                  {'user': 'admin',
                                                   'password': 'admin'},
                                                  '10.10.10.11')
        data_model = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        result, error = JobManager().execute_job(
            target, data_model, action=common.ActionType.CREATE,
            element='vlan_config')
        if result:
            print('Rest job is successful')
        else:
            print('Rest job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task INIT: Driver is not found]'),
                         (result, error))

    def test_execute_ansible_job_timeout_backup(self):
        data_model = self.data_model_1
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            backup_template='playbooks/timeout.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task BACKUP: Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_apply(self):
        data_model = self.data_model_1
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            apply_template='playbooks/timeout.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task APPLY: Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_verify(self):
        data_model = self.data_model_1
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            verify_template='playbooks/timeout.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task VERIFY: Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_job_timeout_rollback(self):
        data_model = self.data_model_1
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, timeout=1,
            apply_template='playbooks/timeout.yaml',
            rollback_template='playbooks/timeout.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task APPLY: Timeout after 1 seconds, '
                                 'Task ROLLBACK: Timeout after 1 seconds]'),
                         (result, error))

    def test_execute_ansible_napalm(self):
        data_model = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  '127.0.0.1')
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/napalm.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_ntc(self):
        data_model = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  '127.0.0.1')
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/ntc.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_job_module_failed(self):
        data_model = {'load_balancer': {'name': 'vLB',
                                        'network-id': 'netABC'}}
        target = self.target_1
        result, error = AnsibleJobManager().execute_job(
            target, data_model, apply_template='playbooks/error_open_file.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        err = "[Task APPLY: {'msg': 'could not locate file in lookup: " \
              "netABC', '_ansible_no_log': None}]"
        self.assertEqual((False, err), (result, error))

    @mock.patch.object(DriverFactory, 'get_driver_dir')
    def test_execute_a10_create_lb(self, mock_method):
        mock_method.return_value = '../drivers/ansible/'
        target = network_function.NetworkFunction('loadbalancer',
                                                  'a10',
                                                  'acos',
                                                  '2.2',
                                                  '10.10.10.11')
        data_model = {'load_balancer': {
            'listeners': [{'name': 'ls1',
                           'pools': ['pl1'],
                           'protocol': 'HTTP',
                           'protocol-port': 8000}],
            'name': 'lb_123',
            'network-id': '764dc206-6f84-4e12-831e-d277ddf6c9c9',
            'pools': [{
                'healthmonitor': {
                    'name': 'test',
                    'protocol': 'HTTP'},
                'lb-algorithm': 'ROUND_ROBIN',
                'members': [{
                    'name': 'name',
                    'protocol-port': 8000}],
                'name': 'pl1',
                'protocol': 'TCP'}],
            'provider': 'octavia'}}
        result, error = JobManager().execute_job(
            target, data_model, action=common.ActionType.CREATE,
            element='loadbalancer')
        if result:
            print('The job is successful')
        else:
            print('The job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task APPLY: {\'msg\': "\'loadbalancer\' '
                                 'is undefined", \'_ansible_no_log\': '
                                 'False}]'),
                         (result, error))

    def test_execute_ansible_vlb_octavia(self):
        data_model = {'loadbalancer':
                          {'name': 'lb_123',
                           'network_id': '764dc206-6f84-4e12-831e',
                           'provider': 'octavia',
                           'listeners': [
                               {'name': 'ls1', 'protocol': 'HTTP',
                                'protocol_port': 8000,
                                'pools': ['pl1']}],
                           'pools': [
                               {'name': 'pl1', 'protocol': 'HTTP',
                                'protocol_port': 8000,
                                'lb_algorithm': 'ROUND_ROBIN',
                                'members': [{
                                    'name': 'name',
                                    'address': "10.60.31.115"
                                }],
                                'healthmonitor':
                                    {
                                        'name': 'test',
                                        'protocol': 'HTTP',
                                        'delay': '10',
                                        'timeout': '5',
                                        'retry_up': '3',
                                        'retry_down': '4'
                                    }
                                }
                           ]
                           }
                      }
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin',
                                                   'auth_url':
                                                       'http://127.0.0.1'},
                                                  'localhost')

        result, error = AnsibleJobManager().execute_job(
            target, data_model,
            apply_template='playbooks/octavia_create_loadbalancer.yaml')
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))
