import sys
import traceback

from networkautomation.drivers.ansible import libansible
from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType


@DriverFactory.register(DriverType.ANSIBLE.value)
class AnsibleDriver(DriverBase):

    def __init__(self, nf: NetworkFunction):
        self.config = {}
        self.config['ssh-host'] = nf.mgmt_ip
        self.config['ssh-user'] = nf.credential['username']
        self.config['ssh-pass'] = nf.credential['password']

    def execute(self, event, target, templates, vars):
        print('===========================================\n'
              'Ansible run event:', event)
        playbook = templates.get(event)
        if playbook:
            config = self.config
            result, error = libansible.execute_playbook(
                playbook,
                config['ssh-host'],
                config['ssh-user'],
                config['ssh-pass'],
                vars
            )
            return error
        else:
            print("Template is not found")
            return None