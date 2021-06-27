import unittest
from unittest import TestCase

from networkautomation import data_model


class TestDataModel(TestCase):
    def test_validate_vlan(self):
        data = {'vlan_config': {'vlan_id': 4094, 'name': 'test'}}
        data_model.DataModel.validate_data(data)

    def test_validate_vlan(self):
        data = {'vlan_config': {'vlan_id': 4095, 'name': 'test'}}
        with self.assertRaises(Exception) as context:
            data_model.DataModel.validate_data(data)
        self.assertTrue('Error in pyangbind datamodel' in str(
            context.exception))

    def test_validate_interface(self):
        data = {'interfaces': {'interface': {'Eth0': {'name':
                               'Eth0', 'config': {'mtu': 9000}}}}}
        data_model.DataModel.validate_data(data)

    def test_validate_loadbalancer(self):
        data = {'load_balancer': {'name': 'vLB'}}
        data_model.DataModel.validate_data(data)

    @unittest.skip
    def test_validate_full_octavia(self):
        data = {'load_balancer':
                    {
                        'listeners': {'0': {'name': 'ls1',
                                       'pools': ['pl1'],
                                       'protocol': 'HTTP',
                                       'protocol-port': 8000}},
                        'name': 'lb_123',
                        'network-id': '764dc206-6f84-4e12-831e-d277ddf6c9c9',
                        'pools': {'0': {
                             'healthmonitor': {'name': 'test', 'protocol': 'HTTP'},
                             'lb-algorithm': 'ROUND_ROBIN',
                             'members': [{'name': 'name', 'protocol-port':
                                 8000}],
                             'name': 'pl1',
                             'protocol': 'TCP'}},
                        'provider': 'octavia'
                    }
                }
        # data = {'load_balancer': {
        #     'listeners': {'name': 'ls1', 'pools': ['pl1'], 'protocol': 'TCP',
        #                   'protocol-port': 8000}, 'name': 'lb_123',
        #     'network-id': '764dc206-6f84-4e12-831e-d277ddf6c9c9',
        #     'pools': {'healthmonitor': {'name': 'test', 'protocol': 'TCP'},
        #               'lb-algorithm': 'ROUND_ROBIN',
        #               'members': [{'name': 'name', 'protocol-port': 8000}],
        #               'name': 'pl1', 'protocol': 'TCP'}, 'provider':
        #         'octavia'}}
        data_model.DataModel.validate_data(data)