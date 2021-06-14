import yaml
from pyangbind.lib import pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder

from networkautomation.pymodels.loadbalancer import loadbalancer
from networkautomation.pymodels.vlan import openconfig_vlan as oc_vlan
from networkautomation.pymodels.interfaces import openconfig_interfaces as \
    oc_interface

class DataModel:
    @classmethod
    def validate_data(self, data, model):
        if model == 'vlan':
            my_obj = oc_vlan()
        elif model == 'interface':
            my_obj = oc_interface()
        elif model == 'loadbalancer':
            my_obj = loadbalancer()
        else:
            raise Exception("Not possible to validate '{}' item".format(model))
        try:
            pybindJSONDecoder.load_json(data, None, None, obj=my_obj,
                path_helper=True, skip_unknown=False)
            out = pybindJSON.dumps(my_obj)
            desc_out = yaml.safe_load(out)
            return desc_out
        except Exception as e:
            raise Exception("Error in pyangbind datamodel: {}".format(str(e)))