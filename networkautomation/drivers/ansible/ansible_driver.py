from networkautomation.drivers.ansible import libansible
from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType


@DriverFactory.register(DriverType.ANSIBLE.value)
class AnsibleDriver(DriverBase):

    def __init__(self, nf: NetworkFunction, element: str = None,
                 driver_name: str = None):
        super().__init__(nf, element, driver_name)
        if nf.credential:
            self.config = nf.credential
            if nf.credential.get('username'):
                self.config['ansible_ssh_user'] = nf.credential['username']
                self.config.pop('username')
            if nf.credential.get('password'):
                self.config['ansible_ssh_pass'] = nf.credential['password']
                self.config.pop('password')

    def execute(self, event, target, templates=None, action=None,
                element=None, input_vars=None):
        print('===========================================\n'
              'Ansible run event:', event)
        extra_vars = {}
        if input_vars:
            extra_vars = input_vars
        if templates:
            playbook = templates.get(event)
        else:
            playbook = self.find_template(event)
            extra_vars['na_action'] = action.value
        if playbook and os.path.exists(playbook):
            result, error = libansible.execute_playbook(
                playbook,
                target.mgmt_ip,
                self.config,
                input_vars=extra_vars,
                tag=element)
            return error
        else:
            print("Template is not found. Skip ...")
            return None

    def find_template(self, event):
        return self.template_dir + '/' + event + '.yaml'
