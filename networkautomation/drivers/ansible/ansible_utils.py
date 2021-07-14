import os
import urllib.request
import zipfile
from pathlib import Path

ANSIBLE_CONFIG_FILE = ".ansible.cfg"
INVENTORY_FILE = "inventory"


def download_package(dir_name, url):
    file_name = 'temp.zip'
    urllib.request.urlretrieve(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall(dir_name)
    os.remove(file_name)


def install_collection(collections_dir, module_name, download_url,
                       unzip_package):
    dir_list = module_name.split('.')
    a10_collection_path = collections_dir
    for dir in dir_list:
        a10_collection_path += '/' + dir
    if not os.path.exists(a10_collection_path):
        dir_tmp = a10_collection_path.replace(dir_list[len(dir_list) - 1], '')
        Path(dir_tmp).mkdir(parents=True, exist_ok=True)
        download_package(dir_tmp, download_url)
        os.rename(dir_tmp + '/' + unzip_package, a10_collection_path)


def download_generate_ansible_cfg(config_file=None):
    home_dir = os.path.expanduser('~')
    if config_file:
        file_path = config_file
    else:
        file_path = home_dir + "/" + ANSIBLE_CONFIG_FILE
    import napalm_ansible
    napalm_module_dir = "{}".format(os.path.dirname(
        napalm_ansible.__file__))
    plugin_paths = napalm_module_dir + '/plugins/action'
    module_paths = napalm_module_dir + '/modules'

    import ntc_ansible_plugin
    module_paths += ':' + os.path.dirname(ntc_ansible_plugin.__file__)

    ansible_collection_dir = home_dir + \
                             '/.ansible/collections/ansible_collections'
    install_collection(ansible_collection_dir, 'a10.acos_axapi',
        'https://codeload.github.com/a10networks/a10-acos-axapi/zip/refs/heads/master',
        'a10-acos-axapi-master')
    plugin_paths += ':' + ansible_collection_dir + \
                    '/a10/acos_axapi/plugins/action'
    module_paths += ':' + ansible_collection_dir + \
                    '/a10/acos_axapi/plugins/modules'

    with open(file_path, 'w') as f:
        f.write('[defaults]\n'
                'host_key_checking=False\n'
                'log_path=/var/log/ansible.log\n'
                'ansible_python_interpreter=\"/usr/bin/env python\"\n'
                'action_plugins={}\n'
                'library={}\n'
                .format(plugin_paths, module_paths))


def create_inventory(host, config, group, inventory_path=INVENTORY_FILE):
    h1 = host + ' ansible_python_interpreter="/usr/bin/env python3" '
    if config:
        for k, v in config.items():
            h1 += k + '=' + str(v) + ' '
    with open(inventory_path, 'w') as f:
        f.write('[{}]\n'.format(group))
        f.write(h1)


def delete_inventory(inventory_path):
    if os.path.exists(inventory_path):
        os.remove(inventory_path)
