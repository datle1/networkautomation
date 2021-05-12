from factory import *

@ExecutorFactory.register('local')
class LocalExecutor(ExecutorBase):

    def run(self, command: str) -> (str, str):
        """ Runs the given command using subprocess """

        stdout, stderr = "abc", "foo"

        out = stdout
        err = stderr
        return out, err

    # end run()

# end class LocalExecutor