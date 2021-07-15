from unittest import TestCase

from networkautomation import network_function

NF = network_function.NetworkFunction(
    'loadbalancer',
    'openstack',
    'octavia',
    '2.0',
    {'username': 'admin',
     'password': 'admin'},
    '10.10.10.10',
    nf_id='24245435'
)


class TestNetworkFunction(TestCase):
    def test_serialize(self):
        json_class = NF.serialize()
        self.assertEqual('{"id": "24245435", '
                         '"type": "loadbalancer", "vendor": "openstack", '
                         '"os": "octavia", "version": "2.0", "mgmt_ip": {'
                         '"username": "admin", "password": "admin"}, '
                         '"ssh_user": "10.10.10.10", "ssh_pass": null, '
                         '"other_auth_info": null, "data_ip": null, '
                         '"metadata": null}', json_class)
        obj_nf = network_function.NetworkFunction.deserialize(json_class)
        self.assertIsInstance(obj_nf, network_function.NetworkFunction)
