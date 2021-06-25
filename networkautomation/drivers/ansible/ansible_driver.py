from networkautomation.drivers.ansible import libansible
from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType


@DriverFactory.register(DriverType.ANSIBLE.value)
class AnsibleDriver(DriverBase):

    def __init__(self, nf: NetworkFunction):
        self.config = {'ssh-host': nf.mgmt_ip,
                       'ssh-user': nf.credential['username'],
                       'ssh-pass': nf.credential['password']}

    def execute(self, event, target, templates, input_vars):
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
                input_vars
            )
            return error
        else:
            print("Template is not found. Skip ...")
            return None
