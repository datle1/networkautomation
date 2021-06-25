from unittest import TestCase
from networkautomation import network_function
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
