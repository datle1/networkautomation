import os
import subprocess
import sys
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
from distutils.sysconfig import get_python_lib


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


def find_data_files(sub_dir):
    data_files = []
    start_point = os.path.join('networkautomation', sub_dir)
    python_dir = get_python_lib()
    for root, dirs, files in os.walk(start_point):
        root_files = [os.path.join(root, i) for i in files]
        data_files.append((python_dir + '/' + root, root_files))
    return data_files


setup(
    name='networkautomation',
    version='0.2',
    python_requires='>=3.6.0',
    packages=find_packages(
        where='.',
        include=['networkautomation*'],
        exclude=['*test*']
    ),
    package_dir={"": "."},
    url='',
    license='',
    author='datlq3',
    author_email='datlq3@viettel.com.vn',
    description='Network Automation Framework',
    data_files=find_data_files('drivers/ansible/templates'),
    cmdclass={'install': NetworkAutomationInstaller},
    install_requires=required
)
