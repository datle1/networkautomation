from networkautomation.drivers.driver_factory import *
from networkautomation.common import DriverType


@DriverFactory.register(DriverType.REST.value)
class RestDriver(DriverBase):

    def execute(self, event, target, job_type, data_model, **kwargs):
        return event
