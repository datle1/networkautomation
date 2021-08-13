import os
import unittest
from unittest import TestCase

from networkautomation import common, job_manager, network_function


def authen_with_env():
    credentials = {}
    try:
        credentials = {
            "auth_url": os.environ['AUTH_URL'],
            "username": os.environ['USER_OCTAVIA'],
            "password": os.environ['PASS_OCTAVIA']
        }
    except KeyError:
        pass
    return credentials


class OctaviaLoadBalancerTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(OctaviaLoadBalancerTest, self).__init__(*args, **kwargs)
        credentials = authen_with_env()
        self.target = network_function.NetworkFunction(nf_type='loadbalancer', vendor='octavia', os='amphora',
                                                       version='2.0', mgmt_ip='localhost',
                                                       other_auth_info=credentials)
        self.job_mgr = job_manager.JobManager()

    @unittest.skip
    def test_create_loadbalancer(self):
        loadbalancer = {
            'admin_state_up': True,
            'name': 'lb_123',
            'address': '10.60.31.58',
            'network_id': '764dc206-6f84-4e12-831e-d277ddf6c9c9',
            'provider': 'octavia',
            'listeners': [
                {
                    'admin_state_up': True,
                    'name': 'ls1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'pool_name': 'pl1',
                }, {
                    'admin_state_up': True,
                    'name': 'ls2',
                    'protocol': 'TCP',
                    'protocol_port': 9999,
                    'pool_name': 'pl2',
                }],
            'pools': [
                {
                    'admin_state_up': True,
                    'name': 'pl1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'lb_algorithm': 'ROUND_ROBIN',
                    'members': [{
                        'admin_state_up': True,
                        'name': 'member1-1',
                        'address': "1.1.1.1"
                    }, {
                        'admin_state_up': True,
                        'name': 'member1-2',
                        'address': "1.1.1.2"
                    }, {
                        'admin_state_up': True,
                        'name': 'member1-3',
                        'address': "1.1.1.3"
                    }],
                    'healthmonitor': {
                        'admin_state_up': True,
                        'name': 'hm1',
                        'protocol': 'HTTP',
                        'delay': '10',
                        'timeout': '5',
                        'retry_up': '3',
                        'retry_down': '4'
                    }
                }, {
                    'admin_state_up': True,
                    'name': 'pl2',
                    'protocol': 'TCP',
                    'protocol_port': 9999,
                    'lb_algorithm': 'ROUND_ROBIN',
                    'members': [{
                        'admin_state_up': True,
                        'name': 'member2-1',
                        'address': "2.2.2.1"
                    }, {
                        'admin_state_up': True,
                        'name': 'member2-2',
                        'address': "2.2.2.2"
                    }, {
                        'admin_state_up': True,
                        'name': 'member2-3',
                        'address': "2.2.2.3"
                    }],
                    'healthmonitor': {
                        'admin_state_up': False,
                        'name': 'hm2',
                        'protocol': 'TCP',
                        'delay': '10',
                        'timeout': '5',
                        'retry_up': '3',
                        'retry_down': '4'
                    }
                }]
        }

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer': loadbalancer},
                                                    action=common.ActionType.CREATE,
                                                    element='loadbalancer',
                                                    timeout=1300)
        self.assertEqual(success, True)

    @unittest.skip
    def test_create_member(self):
        loadbalancer = {
            'name': 'lb_123',
            'pools': [
                {
                    'members': [
                        {
                            'address': '1.1.1.4',
                            'admin_state_up': True,
                            'name': 'member1-4',
                        }],
                    'name': 'pl1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'lb_algorithm': 'ROUND_ROBIN'
                }],
        }

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer': loadbalancer},
                                                    action=common.ActionType.CREATE,
                                                    element='member',
                                                    timeout=1300)
        self.assertEqual(success, True)

    @unittest.skip
    def test_delete_member(self):
        loadbalancer = {
            'name': 'lb_123',
            'pools': [
                {
                    'members': [
                        {
                            'address': '1.1.1.4',
                            'admin_state_up': True,
                            'name': 'member1-4',
                        }],
                    'name': 'pl1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'lb_algorithm': 'ROUND_ROBIN'
                }],
        }

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer': loadbalancer},
                                                    action=common.ActionType.DELETE,
                                                    element='member',
                                                    timeout=1300)
        self.assertEqual(success, True)

    @unittest.skip
    def test_delete_loadbalancer(self):
        loadbalancer = {
            'admin_state_up': True,
            'name': 'lb_123',
            'address': '10.60.31.58',
            'network_id': '764dc206-6f84-4e12-831e-d277ddf6c9c9',
            'provider': 'octavia',
            'listeners': [
                {
                    'admin_state_up': True,
                    'name': 'ls1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'pool_name': 'pl1',
                }, {
                    'admin_state_up': True,
                    'name': 'ls2',
                    'protocol': 'TCP',
                    'protocol_port': 9999,
                    'pool_name': 'pl2',
                }],
            'pools': [
                {
                    'admin_state_up': True,
                    'name': 'pl1',
                    'protocol': 'HTTP',
                    'protocol_port': 8000,
                    'lb_algorithm': 'ROUND_ROBIN',
                    'members': [{
                        'admin_state_up': True,
                        'name': 'member1-1',
                        'address': "1.1.1.1"
                    }, {
                        'admin_state_up': True,
                        'name': 'member1-2',
                        'address': "1.1.1.2"
                    }, {
                        'admin_state_up': True,
                        'name': 'member1-3',
                        'address': "1.1.1.3"
                    }],
                    'healthmonitor': {
                        'admin_state_up': True,
                        'name': 'hm1',
                        'protocol': 'HTTP',
                        'delay': '10',
                        'timeout': '5',
                        'retry_up': '3',
                        'retry_down': '4'
                    }
                }, {
                    'admin_state_up': True,
                    'name': 'pl2',
                    'protocol': 'TCP',
                    'protocol_port': 9999,
                    'lb_algorithm': 'ROUND_ROBIN',
                    'members': [{
                        'admin_state_up': True,
                        'name': 'member2-1',
                        'address': "2.2.2.1"
                    }, {
                        'admin_state_up': True,
                        'name': 'member2-2',
                        'address': "2.2.2.2"
                    }, {
                        'admin_state_up': True,
                        'name': 'member2-3',
                        'address': "2.2.2.3"
                    }],
                    'healthmonitor': {
                        'admin_state_up': False,
                        'name': 'hm2',
                        'protocol': 'TCP',
                        'delay': '10',
                        'timeout': '5',
                        'retry_up': '3',
                        'retry_down': '4'
                    }
                }]
        }

        success, message = self.job_mgr.execute_job(target=self.target,
                                                    data_model={'loadbalancer': loadbalancer},
                                                    action=common.ActionType.DELETE,
                                                    element='loadbalancer',
                                                    timeout=1300)
        self.assertEqual(success, True)
