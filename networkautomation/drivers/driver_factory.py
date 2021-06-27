import json
import os
from typing import Callable
from abc import ABCMeta, abstractmethod
from networkautomation import common
from networkautomation.network_function import NetworkFunction


class DriverFactory:
    """ The factory class for creating drivers"""

    # Key = driver name. Value = driver class
    registry = {}
    # Key = nf_type.vendor.os:element
    # Value = driver name
    profile_map = {}

    TEMPLATE_DIR = 'templates'
    MANIFEST_FILE = 'MANIFEST.json'
    MANIFEST_ELE_ROOT = 'template_info'
    MANIFEST_ELE_SUPPORTED = 'supported_elements'

    """ Internal registry for available drivers """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register Driver class to the internal registry.
        Args:
            name (str): The name of the driver.
        Returns:
            The Driver class itself.
        """
        cls.build_profile_map(name)

        def inner_wrapper(wrapped_class: DriverBase) -> DriverBase:
            if name in cls.registry:
                print('Driver %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_driver(cls, name: str, nf: NetworkFunction, element: str) -> \
            'DriverBase':
        """ Factory command to create the Driver.
        This method gets the appropriate Driver class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the Driver to create.
            nf (NetworkFunction): A object of Network Function.
        Returns:
            An instance of the Driver that is created.
        """

        if name not in cls.registry:
            print('Driver %s does not exist in the registry' % name)
            return None

        exec_class = cls.registry[name]
        driver = exec_class(nf, element=element, driver_name=name)
        return driver

    @classmethod
    def get_driver_name(cls, nf: NetworkFunction, element: str) -> (str):
        profile_name = cls.generate_profile_name(nf, element)
        if profile_name not in cls.profile_map:
            print('Profile %s does not exist in the registry' % profile_name)
            return None
        return cls.profile_map.get(profile_name)

    @classmethod
    def generate_profile_name(cls, nf, element):
        return nf.type + '.' + nf.vendor + '.' + nf.os + ':' + element

    @classmethod
    def build_profile_map(cls, name):
        if name == common.DriverType.ANSIBLE.value:
            profile_list = cls.scan_dir_for_ansible_profile(
                cls.get_driver_dir(name) + cls.TEMPLATE_DIR)
            for key in profile_list:
                cls.profile_map[key] = common.DriverType.ANSIBLE.value
        return cls.profile_map

    @classmethod
    def scan_dir_for_ansible_profile(cls, root_dir):
        profile_list = []
        import glob
        for path in glob.glob(f'{root_dir}/*/*/*/', recursive=False):
            with open(path + '/' + cls.MANIFEST_FILE, 'r') as f:
                content = json.load(f)
            supported_elements = content[cls.MANIFEST_ELE_ROOT][
                cls.MANIFEST_ELE_SUPPORTED]
            temp = path.replace(root_dir, '')[1:-1].replace('/', '.')
            for ele in supported_elements:
                profile_list.append(temp + ':' + ele)
        return profile_list

    @classmethod
    def get_driver_dir(cls, name):
        import networkautomation
        module_path = os.path.dirname(networkautomation.__file__)
        return module_path + '/drivers/' + name + '/'


class DriverBase(metaclass=ABCMeta):
    """ Base class for an Driver """
    template_dir = ''

    def __init__(self, nf: NetworkFunction, element: str = None,
                 driver_name: str = None):
        """ Constructor """
        if element and driver_name:
            profile_name = DriverFactory.generate_profile_name(nf, element)
            self.template_dir = DriverFactory.get_driver_dir(driver_name) + \
                                DriverFactory.TEMPLATE_DIR + '/' + \
                                profile_name.split(':')[0].replace('.', '/')

    @abstractmethod
    def execute(self, **kwargs) -> (str):
        """ Abstract method to process a input """
        pass
