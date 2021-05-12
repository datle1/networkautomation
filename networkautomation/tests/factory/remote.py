from factory import *

@ExecutorFactory.register('remote')
class RemoteExecutor(ExecutorBase):

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    # end __init__()

    def run(self, command: str) -> (str, str):
        """ Runs the command using paramiko """

        # Creates the client, connects and issues the command
        out = "123"
        err = "endless"
        return out, err

    # end run()

# end class RemoteExecutor