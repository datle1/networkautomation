from unittest import TestCase
from networkautomation import network_function
from networkautomation.drivers.ansible.ansible_driver import AnsibleDriver


class TestAnsibleDriver(TestCase):
    def test_init(self):
        target = network_function.NetworkFunction('vloadbalancer',
                                                  'openstack',
                                                  'octavia',
                                                  '2.0',
                                                  'localhost',
                                                  ssh_user='admin',
                                                  ssh_pass='password',
                                                  other_auth_info={
                                                      'auth_url': 'url',
                                                      'domain': 'default'})
        ad = AnsibleDriver(target)
        expect = {'ansible_ssh_pass': 'password',
                  'ansible_ssh_user': 'admin',
                  'auth_url': 'url',
                  'domain': 'default'}
        self.assertEqual(ad.config, expect)
