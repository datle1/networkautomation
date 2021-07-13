from unittest import TestCase

from networkautomation import network_function

NF = network_function.NetworkFunction(
    'vloadbalancer',
    'openstack',
    'octavia',
    '2.0',
    {'username': 'admin',
     'password': 'admin'},
    '10.10.10.10'
)


class TestNetworkFunction(TestCase):
    def test_serialize(self):
        dict = NF.serialize()
        print(dict)
        obj_nf = network_function.NetworkFunction.deserialize(dict)
        print(obj_nf)
        dict = obj_nf.serialize()
        print(dict)
