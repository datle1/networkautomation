import json

from networkautomation import utils


class NetworkFunction:
    def __init__(self, type, vendor, os, 
                    version, credential, mgmt_ip,
                    data_ip=None, metadata=None, id=None):
        self.id = id or utils.gen_uuid()
        self.type = type
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
        dict = json.JSONDecoder().decode(dict_str)
        return NetworkFunction(dict['type'], dict['vendor'], dict['os'],
                    dict['version'], dict['credential'], dict['mgmt_ip'],
                    data_ip=dict['data_ip'], metadata=dict['metadata'],
                     id=dict['id'])

    def to_dict(self):
        return self.__dict__