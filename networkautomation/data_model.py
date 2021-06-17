import yaml
from pyangbind.lib import pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
from networkautomation.pymodels.network_models import network_models


class DataModel:
    @classmethod
    def validate_data(self, data):
        my_obj = network_models()
        try:
            pybindJSONDecoder.load_json(data, None, None, obj=my_obj,
                path_helper=True, skip_unknown=False)
            out = pybindJSON.dumps(my_obj)
            desc_out = yaml.safe_load(out)
            return desc_out
        except Exception as e:
            raise Exception("Error in pyangbind datamodel: {}".format(str(e)))