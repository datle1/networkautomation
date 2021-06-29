from networkautomation.drivers.ansible import libansible
from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType


@DriverFactory.register(DriverType.ANSIBLE.value)
class AnsibleDriver(DriverBase):

    def __init__(self, nf: NetworkFunction, element: str = None,
                 driver_name: str = None):
        super().__init__(nf, element, driver_name)
        self.config = {'ssh-host': nf.mgmt_ip,
                       'ssh-user': None,
                       'ssh-pass': None,
                       'extra': None}
        if nf.credential:
            if nf.credential.get('auth_url'):
                self.config['extra'] = ''
                for k, v in nf.credential.items():
                    self.config['extra'] += k + '=' + v + ' '
            elif nf.credential.get('username') \
                    and nf.credential.get('password'):
                self.config['ssh-user'] = nf.credential['username']
                self.config['ssh-pass'] = nf.credential['password']

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
                self.config['ssh-host'],
                self.config['ssh-user'],
                self.config['ssh-pass'],
                extra_config=self.config['extra'],
                input_vars=extra_vars,
                tag=element)
            return error
        else:
            print("Template is not found. Skip ...")
            return None

    def find_template(self, event):
        return self.template_dir + '/' + event + '.yaml'
