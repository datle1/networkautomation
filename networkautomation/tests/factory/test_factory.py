#!/usr/bin/env python

# Standard imports
import os
import unittest
from unittest import TestCase, mock
from factory import *

# Application imports
from networkautomation.drivers.driver_factory import DriverFactory


if __name__ == '__main__':

    # Creates a local executor
    local = ExecutorFactory.create_executor('local')
    local_out = local.run('ls -ltra')
    print(local_out)

    remote = ExecutorFactory.create_executor('remote')
    remote_out = remote.run('ls -ltra')
    print(remote_out)


class TestDriverFactory(TestCase):

    @mock.patch.object(DriverFactory, 'get_driver_dir')
    def test_scan_dir_for_ansible_profile(self, mock_method):
        print(os.getcwd())
        mock_method.return_value = '../../drivers/ansible/'
        map = DriverFactory.build_profile_map('ansible')
        print(map)

    @unittest.skip
    def test_get_driver_dir(self):
        print(DriverFactory.get_driver_dir('ansible'))
