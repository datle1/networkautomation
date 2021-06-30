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
                                                   'ssh-password': 'admin'},
                                                  'localhost')
        ad = AnsibleDriver(target)
        expect = {'ansible_ssh_pass': 'admin', 'auth_url': 'url'}
        self.assertEqual(ad.config, expect)
