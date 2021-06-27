from networkautomation.drivers.driver_factory import DriverFactory
# Import all drivers to load decorator
from networkautomation.drivers.ansible import ansible_driver
from networkautomation.drivers.rest import rest_driver


def get_driver(driver_type, target, element):
    if driver_type:
        driver_name = driver_type.value
    else:
        driver_name = DriverFactory.get_driver_name(target, element)
        if not driver_name:
            return None
    return DriverFactory.create_driver(name=driver_name, nf=target,
        element=element)
