#!/usr/bin/env python

# Standard imports

from factory import *

# Application imports


if __name__ == '__main__':

    # Creates a local executor
    local = ExecutorFactory.create_executor('local')
    local_out = local.run('ls -ltra')
    print(local_out)

    remote = ExecutorFactory.create_executor('remote')
    remote_out = remote.run('ls -ltra')
    print(remote_out)
