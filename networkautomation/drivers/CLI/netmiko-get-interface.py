from netmiko import ConnectHandler
import re

#from device_info import ios_xe1 as device # noqa
from networkautomation import network_function as device
# Create a CLI command template
show_interface_config_temp = "show running-config interface {}"

# Open CLI connection to device
with ConnectHandler(ip = device["address"],
                    port = device["ssh_port"],
                    username = device["username"],
                    password = device["password"],
                    device_type = device["device_type"]) as ch:

    # Create desired CLI command and send to device
    command = show_interface_config_temp.format("Loopback103")
    interface = ch.send_command(command)

    # Print the raw command output to the screen
    print(interface)

    try:
        # Use regular expressions to parse the output for desired data
        name = re.search(r'interface (.*)', interface).group(1)
        description = re.search(r'description (.*)', interface).group(1)
        ip_info = re.search(r'ip address (.*) (.*)', interface)
        ip = ip_info.group(1)
        netmask = ip_info.group(2)

        # Print the info to the screen
        print("The interface {name} has ip address {ip}/{mask}".format(
                name = name,
                ip = ip,
                mask = netmask,
                )
            )
    except Exception:
        print("There was an error, Loopback103 might not exist.")