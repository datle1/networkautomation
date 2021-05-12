from unittest import TestCase

from networkautomation import common, job_manager, network_function

class Test(TestCase):
    def test_execute_ansible_job(self):
        playbooks = {
            'APPLY': 'playbooks/apply.yaml',
            # 'BACKUP': '/home/dat/networkautomation/networkautomation'
            #          '/drivers/ansible/playbooks/timeout.yaml',
            # 'ROLLBACK' : '/home/dat/networkautomation/networkautomation'
            #          '/drivers/ansible/playbooks/rollback.yaml',
            # 'VERIFY' : '/home/dat/networkautomation/networkautomation'
            #          '/drivers/ansible/playbooks/verify.yaml'
        }
        vars = {'file_name': '/tmp/foo'}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'dat',
                                                   'password': 'dat'},
                                                  '127.0.0.1')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING, target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks, vars=vars,
                                             timeout=180)
        if result == True:
            print("Ansible job is successful")
        else:
            print("Ansible job is failed. Reason: " + error)


    def test_execute_rest_job(self):
        target = network_function.NetworkFunction('firewall',
                                                  'fortinet',
                                                  'fortios',
                                                  '7.1',
                                                  {'user': 'admin', 'password': 'admin'},
                                                  '10.10.10.11')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.CONFIGURATION,
                                             target, role='vlan',
                                             action=common.ActionType.CREATE)
        if result == True:
            print("Rest job is successful")
        else:
            print("Rest job is failed. Reason: " + error)


    def test_execute_ansible_job_timeout(self):
        playbooks = {
            'BACKUP': 'playbooks/timeout.yaml'
        }
        vars = {'vlan_id': 123}
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  '10.10.10.10')
        job_mgmt = job_manager.JobManager()
        result, error = job_mgmt.execute_job(common.JobType.PROVISIONING, target,
                                             common.DriverType.ANSIBLE,
                                             templates=playbooks, vars=vars,
                                             timeout=1)
        if result == True:
            print("Ansible job is successful")
        else:
            print("Ansible job is failed. Reason: " + error)