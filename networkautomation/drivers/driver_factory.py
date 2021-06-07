from typing import Callable
from abc import ABCMeta, abstractmethod

from networkautomation.network_function import NetworkFunction


class DriverFactory:
    """ The factory class for creating drivers"""

    # Key = driver name. Value = driver class
    registry = {}
    # Key = job_type.object:backup|apply|verify|rollback
    # Value = driver name
    profile_map = {}

    """ Internal registry for available drivers """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register Driver class to the internal registry.
        Args:
            name (str): The name of the driver.
        Returns:
            The Driver class itself.
        """

        def inner_wrapper(wrapped_class: DriverBase) -> DriverBase:
            if name in cls.registry:
                print('Driver %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    @classmethod
    def create_driver(cls, name: str, nf: NetworkFunction) -> 'DriverBase':
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
        driver = exec_class(nf)
        return driver

    @classmethod
    def get_driver(cls, element: str, action: str, nf: NetworkFunction) -> (str):
        profile_name = nf.type + '.' + nf.vendor + '.' + nf.os + '.' \
                       + nf.version + ':' + element + ':' + action
        if profile_name not in cls.profile_map:
            print('Profile %s does not exist in the registry' % profile_name)
            return None
        return cls.profile_map.get(profile_name)


class DriverBase(metaclass=ABCMeta):
    """ Base class for an Driver """

    @abstractmethod
    def __init__(self, nf: NetworkFunction):
        """ Constructor """
        pass

    @abstractmethod
    def execute(self, **kwargs) -> (str):
        """ Abstract method to process a input """
        pass
