import json

from networkautomation import utils


class NetworkFunction:
    def __init__(self, nf_type, vendor, os,
                 version, credential, mgmt_ip,
                 data_ip=None, metadata=None, nf_id=None):
        self.id = nf_id or utils.gen_uuid()
        self.type = nf_type
        self.vendor = vendor
        self.os = os
        self.version = version
        self.credential = credential
        self.mgmt_ip = mgmt_ip
        self.data_ip = data_ip
        self.metadata = metadata

    def serialize(self):
        return json.JSONEncoder().encode(self.__dict__)

    @classmethod
    def deserialize(cls, dict_str):
        temp = json.JSONDecoder().decode(dict_str)
        return NetworkFunction(temp['type'], temp['vendor'], temp['os'],
                               temp['version'], temp['credential'],
                               temp['mgmt_ip'], data_ip=temp['data_ip'],
                               metadata=temp['metadata'], nf_id=temp['id'])

    def to_dict(self):
        return self.__dict__
