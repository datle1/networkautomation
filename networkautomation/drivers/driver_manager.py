from networkautomation.drivers.driver_factory import DriverFactory
# Import all drivers to load decorator
from networkautomation.drivers.ansible import ansible_driver
from networkautomation.drivers.rest import rest_driver


def get_driver_from_name(driver_type, target):
    return DriverFactory.create_driver(name=driver_type, nf=target)


def get_driver_from_state(element, state, target):
    driver_type = DriverFactory.get_driver(element, state, target)
    if not driver_type:
        return None
    return get_driver_from_name(driver_type, target)
