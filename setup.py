from setuptools import setup
from setuptools import find_packages

setup(
    name='networkautomation',
    version='0.2',
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
    install_requires=[
        'ansible',
        'psutil',
        'pyangbind',
        'napalm-ansible',
        'ntc-ansible',
    ]
)
