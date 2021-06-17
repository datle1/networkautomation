from unittest import TestCase

from networkautomation import data_model


class TestDataModel(TestCase):
    def test_validate_vlan(self):
        data = {'vlan-config': {'vlan-id': 4094, 'name': 'test'}}
        data_model.DataModel.validate_data(data)

    def test_validate_interface(self):
        data = {'interfaces': {'interface': {'Eth0': {'name':
                               'Eth0', 'config': {'mtu': 9000}}}}}
        data_model.DataModel.validate_data(data)

    def test_validate_loadbalancer(self):
        data = {'loadbalancer': {'name': 'vLB'}}
        data_model.DataModel.validate_data(data)