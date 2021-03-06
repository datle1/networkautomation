import os
import subprocess
import sys

from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install


class NetworkAutomationInstaller(install):
    """Generation of .py files from yang models and setup ntc-ansible module"""
    model_file = "/models/network-models.yang"
    pymodel_file = "/networkautomation/pymodels/network_models.py"

    def pip_install(self, package):
        subprocess.call([sys.executable, "-m", "pip", "install", package])

    def run(self):
        working_dir = os.getcwd()
        print("Working dir: {} ".format(working_dir))
        self.pip_install("pyangbind")
        import pyangbind
        pyangbind_path = os.path.dirname(pyangbind.__file__) + '/plugin'
        protoc_command = ["pyang",
                          "-p",
                          "models",
                          "--plugindir",
                          pyangbind_path,
                          "-f",
                          "pybind",
                          "-o",
                          working_dir + self.pymodel_file,
                          working_dir + self.model_file]
        if subprocess.call(protoc_command) != 0:
            sys.exit(-1)
        install.run(self)


with open('requirements.txt') as f:
    required = f.read().splitlines()
print('Requirements: {}'.format(required))


def find_package_data(root):
    directory = os.path.join(root, 'drivers/ansible/templates')
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='networkautomation',
    version='0.3',
    python_requires='>=3.6.0',
    packages=find_packages(),
    url='',
    license='',
    author='datlq3',
    author_email='datlq3@viettel.com.vn',
    description='Network Automation Framework',
    package_data={
        '': find_package_data('networkautomation')
    },
    cmdclass={'install': NetworkAutomationInstaller},
    install_requires=required
)
