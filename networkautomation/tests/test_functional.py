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
        extra_vars = {'loadbalancer': {'name': 'vLB'}}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             element='loadbalancer',
                                             extra_vars=extra_vars,
                                             timeout=180)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (True, None))

    def test_execute_rest_job(self):
        target = network_function.NetworkFunction('firewall',
                                                  'fortinet',
                                                  'fortios',
                                                  '7.1',
                                                  {'user': 'admin',
                                                   'password': 'admin'},
                                                  '10.10.10.11')
        job_mgmt = job_manager.JobManager()
        extra_vars = {'vlan-config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        result, error = job_mgmt.execute_job(common.JobType.CONFIGURATION,
                                             target, element='vlan',
                                             extra_vars=extra_vars,
                                             action=common.ActionType.CREATE)
        if result:
            print('Rest job is successful')
        else:
            print('Rest job is failed. Reason: ' + error)
        self.assertEqual((result, error), (True, None))

    def test_execute_ansible_job_timeout_backup(self):
        playbooks = {
            'BACKUP': 'playbooks/timeout.yaml'
        }
        extra_vars = {'vlan_id': 123}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             extra_vars=extra_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (False, 'Task BACKUP got timeout| '))

    def test_execute_ansible_job_timeout_apply(self):
        playbooks = {
            'APPLY': 'playbooks/timeout.yaml'
        }
        extra_vars = {'vlan_id': 123}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             extra_vars=extra_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (False, 'Task APPLY got timeout| '))

    def test_execute_ansible_job_timeout_verify(self):
        playbooks = {
            'VERIFY': 'playbooks/timeout.yaml'
        }
        extra_vars = {'vlan_id': 123}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             extra_vars=extra_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (False, 'Task VERIFY got timeout| '))

    def test_execute_ansible_job_timeout_rollback(self):
        playbooks = {
            'APPLY': 'playbooks/timeout.yaml',
            'ROLLBACK': 'playbooks/timeout.yaml'
        }
        extra_vars = {'vlan_id': 123}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             extra_vars=extra_vars,
                                             timeout=1)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (False, 'Task APPLY got timeout| '
                                                  'Task ROLLBACK got timeout| '))

    def test_execute_ansible_napalm(self):
        playbooks = {
            'APPLY': 'playbooks/napalm.yaml',
        }
        extra_vars = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             element='vlan',
                                             extra_vars=extra_vars)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (True, None))

    def test_execute_ansible_ntc(self):
        playbooks = {
            'APPLY': 'playbooks/ntc.yaml',
        }
        extra_vars = {'vlan_config': {'vlan-id': 4094, 'name': 'vlanTest'}}
        target = network_function.NetworkFunction('switch',
                                                  'arista',
                                                  'eos',
                                                  '4.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING,
                                             target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks,
                                             element='vlan',
                                             extra_vars=extra_vars)
        if result:
            print('Ansible job is successful')
        else:
            print('Ansible job is failed. Reason: ' + error)
        self.assertEqual((result, error), (True, None))