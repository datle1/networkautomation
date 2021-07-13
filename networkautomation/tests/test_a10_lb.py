import os
import unittest
from unittest import TestCase

from networkautomation import common, job_manager, network_function


def creds_from_env():
    creds, mgmt_ip, missing = {}, '', True
    try:
        creds = {'ansible_username': os.environ['ANSIBLE_USERNAME'],
                 'ansible_password': os.environ['ANSIBLE_PASSWORD'],
                 'ansible_port': os.environ['ANSIBLE_PORT']}
        mgmt_ip = os.environ['ANSIBLE_HOST']
        missing = False
    except KeyError:
        pass
    return creds, mgmt_ip, missing


_, _, skip_test = creds_from_env()


class A10LoadBalancerTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(A10LoadBalancerTest, self).__init__(*args, **kwargs)
        creds, mgmt_ip, _ = creds_from_env()
        self.target = network_function.NetworkFunction(nf_type='loadbalancer', vendor='a10', os='acos',
                                                       version=None, mgmt_ip=mgmt_ip,
                                                       credential=creds)
        self.job_mgr = job_manager.JobManager()

    @unittest.skipIf(skip_test, 'Ansible variables are not provided.')
    def test_create_loadbalancer(self):
        loadbalancer = {'address': '10.61.123.211',
                        'admin_state_up': True,
                        'listeners': [{'admin_state_up': True,
                                       'connection_limit': 10,
                                       'name': 'listener1',
                                       'pool_name': 'pool1',
                                       'protocol': 'HTTP',
                                       'protocol_port': 9999}],
                        'name': 'lb1',
                        'pools': [{'admin_state_up': True,
                                   'healthmonitor': {'admin_state_up': True,
                                                     'delay': 5,
                                                     'name': 'hm1',
                                                     'protocol': 'TCP',
                                                     'retry_down': 4,
                                                     'retry_up': 3,
                                                     'timeout': 2},
                                   'lb_algorithm': 'ROUND_ROBIN',
                                   'members': [{'address': '2.2.2.1',
                                                'admin_state_up': True,
                                                'name': 'member1',
                                                'weight': 1},
                                               {'address': '2.2.2.2',
                                                'admin_state_up': True,
                                                'name': 'member2',
                                                'weight': 1},
                                               {'address': '2.2.2.3',
                                                'admin_state_up': True,
                                                'name': 'member3',
                                                'weight': 1}],
                                   'name': 'pool1',
                                   'protocol': 'TCP',
                                   'protocol_port': 80}],
                        'project_id': '',
                        'provider': 'a10',
                        'vip_network_input': ''}

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer':
                                                                    loadbalancer},
                                                    action=common.ActionType.CREATE,
                                                    element='loadbalancer',
                                                    timeout=1000)
        self.assertEqual(success, True)

    @unittest.skipIf(skip_test, 'Ansible variables are not provided.')
    def test_create_member(self):
        loadbalancer = {'name': 'lb1',
                        'pools': [{'members': [{'address': '2.2.2.4',
                                                'admin_state_up': True,
                                                'name': 'member4',
                                                'weight': 1}],
                                   'name': 'pool1',
                                   'protocol': 'TCP',
                                   'protocol_port': 80}],
                        'provider': 'a10'}

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer':
                                                                    loadbalancer},
                                                    action=common.ActionType.CREATE,
                                                    element='member',
                                                    timeout=1000)
        self.assertEqual(success, True)

    @unittest.skipIf(skip_test, 'Ansible variables are not provided.')
    def test_delete_member(self):
        loadbalancer = {'name': 'lb1',
                        'pools': [{'members': [{'address': '2.2.2.4',
                                                'admin_state_up': True,
                                                'name': 'member4',
                                                'weight': 1}],
                                   'name': 'pool1',
                                   'protocol': 'TCP',
                                   'protocol_port': 80}],
                        'provider': 'a10'}

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer':
                                                                    loadbalancer},
                                                    action=common.ActionType.DELETE,
                                                    element='member',
                                                    timeout=1000)
        self.assertEqual(success, True)

    @unittest.skipIf(skip_test, 'Ansible variables are not provided.')
    def test_delete_loadbalancer(self):
        loadbalancer = {'address': '10.61.123.211',
                        'admin_state_up': True,
                        'listeners': [{'admin_state_up': True,
                                       'connection_limit': 10,
                                       'name': 'listener1',
                                       'pool_name': 'pool1',
                                       'protocol': 'HTTP',
                                       'protocol_port': 9999}],
                        'name': 'lb1',
                        'pools': [{'admin_state_up': True,
                                   'healthmonitor': {'admin_state_up': True,
                                                     'delay': 5,
                                                     'name': 'hm1',
                                                     'protocol': 'HTTP',
                                                     'retry_down': 4,
                                                     'retry_up': 3,
                                                     'timeout': 2},
                                   'lb_algorithm': 'ROUND_ROBIN',
                                   'members': [{'address': '2.2.2.1',
                                                'admin_state_up': True,
                                                'name': 'member1',
                                                'weight': 1},
                                               {'address': '2.2.2.2',
                                                'admin_state_up': True,
                                                'name': 'member2',
                                                'weight': 1},
                                               {'address': '2.2.2.3',
                                                'admin_state_up': True,
                                                'name': 'member3',
                                                'weight': 1}],
                                   'name': 'pool1',
                                   'protocol': 'TCP',
                                   'protocol_port': 80}],
                        'project_id': '',
                        'provider': 'a10',
                        'vip_network_input': ''}

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer':
                                                                    loadbalancer},
                                                    action=common.ActionType.DELETE,
                                                    element='loadbalancer',
                                                    timeout=1000)
        self.assertEqual(success, True)
