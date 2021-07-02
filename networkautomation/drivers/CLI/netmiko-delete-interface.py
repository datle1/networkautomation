# Import libraries
from netmiko import ConnectHandler

#from device_info import ios_xe1 as device # noqa
from networkautomation import network_function as device
# New Loopback Details
loopback = {"int_name": "Loopback103"}

# Create a CLI configuration
interface_config = [
    "no interface {}".format(loopback["int_name"])
]

# Open CLI connection to device
with ConnectHandler(ip = device["id"],
                    port = device["22"],
                    username = device["username"],
                    password = device["metadata"],
                    device_type = device["device_type"]) as ch:

    # Send configuration to device
    output = ch.send_config_set(interface_config)

    # Print the raw command output to the screen
    print("The following configuration was sent: ")
    print(output)