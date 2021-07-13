from networkautomation.drivers.ansible import libansible
from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType, JobType


@DriverFactory.register(DriverType.ANSIBLE.value)
class AnsibleDriver(DriverBase):
    NA_ACTION = 'na_action'

    def __init__(self, nf: NetworkFunction, element: str = None,
                 driver_name: str = None):
        super().__init__(nf, element, driver_name)
        self.config = {}
        if nf.other_auth_info:
            self.config = nf.other_auth_info
        if nf.ssh_user:
            self.config['ansible_ssh_user'] = nf.ssh_user
        if nf.ssh_pass:
            self.config['ansible_ssh_pass'] = nf.ssh_pass

    def execute(self, event, target, job_type, data_model, **kwargs):
        print('===========================================\n'
              'Ansible run event:', event)
        extra_vars = data_model
        tags = []
        if job_type == JobType.USE_TEMPLATE:
            # Use user-defined templates
            playbook = kwargs.get(event.lower() + '_template')
            if kwargs.get('extra_vars'):
                extra_vars.update(kwargs.get('extra_vars'))
            if kwargs.get('tags'):
                tags = kwargs.get('tags')
        else:
            # Use framework 's exited templates
            playbook = self.find_template(event)
            extra_vars[self.NA_ACTION] = kwargs.get('action').value
            tags.append(kwargs.get('element'))
        if playbook and os.path.exists(playbook):
            result, error = libansible.execute_playbook(
                playbook,
                target.mgmt_ip,
                self.config,
                input_vars=extra_vars,
                tags=tags)
            return error
        else:
            print("Template is not found. Skip ...")
            return None

    def find_template(self, event):
        return self.template_dir + '/' + event + '.yaml'
