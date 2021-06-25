from typing import Callable
from abc import ABCMeta, abstractmethod

class ExecutorFactory:
    """ The factory class for creating executors"""

    registry = {}
    """ Internal registry for available executors """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register Executor class to the internal registry.
        Args:
            name (str): The name of the executor.
        Returns:
            The Executor class itself.
        """

        def inner_wrapper(wrapped_class: ExecutorBase) -> Callable:
            if name in cls.registry:
                print('Executor %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create_executor(cls, name: str, **kwargs) -> 'ExecutorBase':
        """ Factory command to create the executor.
        This method gets the appropriate Executor class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the executor to create.
        Returns:
            An instance of the executor that is created.
        """

        if name not in cls.registry:
            print('Executor %s does not exist in the registry', name)
            return None

        exec_class = cls.registry[name]
        executor = exec_class(**kwargs)
        return executor

    # end create_executor()

# end class ExecutorFactory


class ExecutorBase(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    @abstractmethod
    def run(self, command: str) -> (str, str):
        """ Abstract method to run a command """
        pass

# end class ExecutorBase