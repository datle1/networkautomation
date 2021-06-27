import unittest
from unittest import TestCase
from networkautomation import network_function
from networkautomation.common import ActionType
from networkautomation.drivers.ansible.ansible_driver import AnsibleDriver


class TestAnsibleDriver(TestCase):
    def test_init(self):
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  {'auth_url': 'url',
                                                   'password': 'admin'},
                                                  'localhost')
        ad = AnsibleDriver(target)
        expect = {'ssh-host': 'localhost',
                  'ssh-user': None,
                  'ssh-pass': None,
                  'extra': 'auth_url=url password=admin '}
        self.assertEqual(ad.config, expect)

    @unittest.skip
    def test_execute(self):
        target = network_function.NetworkFunction('loadbalancer',
                                                  'a10',
                                                  'acos',
                                                  '2.0',
                                                  {'username': 'admin',
                                                   'password': 'admin'},
                                                  'localhost')
        input_vars = {'loadbalancer': {
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
                        'provider': 'a10'}
                    }
        ad = AnsibleDriver(target, element='loadbalancer',
            driver_name='ansible')
        result = ad.execute('APPLY', target, action=ActionType.CREATE,
            element='loadbalancer', input_vars=input_vars)
        self.assertEqual(result, 'expect')
