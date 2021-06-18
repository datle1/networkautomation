from unittest import TestCase
from networkautomation import common, job_manager, network_function


class FunctionalTest(TestCase):

    def test_execute_ansible_job(self):
        playbooks = {
            'APPLY': 'playbooks/apply.yaml',
            # 'BACKUP': 'playbooks/backup.yaml',
            # 'ROLLBACK' : 'playbooks/rollback.yaml',
            # 'VERIFY' : 'playbooks/verify.yaml'
        }
        input_vars = {'loadbalancer': {'name': 'vLB'}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=180)
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
        job_mgmt = job_manager.JobManager()
        input_vars = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        result, error = job_mgmt.execute_job(common.JobType.USE_ACTION,
                                             target,
                                             action=common.ActionType.CREATE,
                                             element='vlan_config',
                                             input_vars=input_vars)
        if result:
            print('Rest job is successful')
        else:
            print('Rest job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task BACKUP: Driver is not found]'),
                        (result, error))

    def test_execute_ansible_job_timeout_backup(self):
        playbooks = {
            'BACKUP': 'playbooks/timeout.yaml'
        }
        input_vars = {'vlan_config': {'vlan_id': 123}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task BACKUP: Timeout]'),
                        (result, error))

    def test_execute_ansible_job_timeout_apply(self):
        playbooks = {
            'APPLY': 'playbooks/timeout.yaml'
        }
        input_vars = {'vlan_config': {'vlan_id': 123}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task APPLY: Timeout]'), (result, error))

    def test_execute_ansible_job_timeout_verify(self):
        playbooks = {
            'VERIFY': 'playbooks/timeout.yaml'
        }
        input_vars = {'vlan_config': {'vlan_id': 123}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task VERIFY: Timeout]'), (result, error))

    def test_execute_ansible_job_timeout_rollback(self):
        playbooks = {
            'APPLY': 'playbooks/timeout.yaml',
            'ROLLBACK': 'playbooks/timeout.yaml'
        }
        input_vars = {'vlan_config': {'vlan_id': 123}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((False, '[Task APPLY: Timeout, '
                                 'Task ROLLBACK: Timeout]'), (result, error))

    def test_execute_ansible_napalm(self):
        playbooks = {
            'APPLY': 'playbooks/napalm.yaml',
        }
        input_vars = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_ntc(self):
        playbooks = {
            'APPLY': 'playbooks/ntc.yaml',
        }
        input_vars = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((True, None), (result, error))

    def test_execute_ansible_job_module_failed(self):
        playbooks = {
            'APPLY': 'playbooks/error_open_file.yaml',
        }
        input_vars = {'loadbalancer': {'name': 'vLB'}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'dat',
                                                   'password': 'dat'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.USE_TEMPLATE,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             input_vars=input_vars,
                                             timeout=180)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        file_name = str.encode(input_vars.get("loadbalancer").get("name"))
        err = "[Task APPLY: ['could not locate file in lookup: vLB']]"\
            .format(file_name)
        self.assertEqual((False, err), (result, error))
