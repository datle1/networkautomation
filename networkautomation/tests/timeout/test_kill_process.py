import os
import unittest
from unittest import TestCase
import psutil

class ProcessTest(TestCase):
    @unittest.skip
    def test_timeout(self):
        current_process = psutil.Process(pid=19450)
        children = current_process.children(recursive=True)
        for child in children:
            print('Child pid is {}'.format(child.pid))
            os.kill(int(child.pid), int(15))