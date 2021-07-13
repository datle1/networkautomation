import time

from networkautomation.common import JobState, DriverType, JobType, ActionType
from networkautomation import job
from networkautomation.network_function import NetworkFunction

"""Network Automation Framework
   Exposed module to executing network automation jobs.
"""


class BaseJobManager:
    JOB_POOL = {}
    DEFAULT_JOB_TIMEOUT = 3 * 60  # seconds

    def execute_job(self, job_type, target, data_model,
                    timeout=DEFAULT_JOB_TIMEOUT, **kwargs):
        my_job = job.Job(job_type, target, data_model, **kwargs)
        if my_job:
            self.JOB_POOL[my_job.id] = my_job
            return my_job.execute(timeout)
        else:
            return False, 'Error: can not init job'

    def register_job(self, job_type, target, data_model, **kwargs):
        my_job = job.Job(job_type, target, data_model, **kwargs)
        if my_job:
            self.JOB_POOL[my_job.id] = my_job
            return my_job.id
        else:
            print('Can not init job')
            return None

    def start_job(self, job_id, timeout=DEFAULT_JOB_TIMEOUT):
        my_job = self.JOB_POOL.get(job_id)
        if my_job:
            my_job.execute(timeout)
        else:
            print('Can not find job ', job_id)

    def wait_to_finish_job(self, job_id, timeout=None, auto_terminate=True):
        my_job = self.JOB_POOL.get(job_id)
        timeout_microsecond = 0
        if timeout:
            timeout_microsecond = timeout * 1000000
        begin_time = time.time()
        while my_job.status != JobState.FINISHED:
            if (timeout_microsecond > 0) \
                    and (time.time() - begin_time >= timeout_microsecond):
                if auto_terminate:
                    my_job.terminate()
                break
            else:
                time.sleep(2)

    def terminate_job(self, job_id):
        if job_id in self.JOB_POOL:
            my_job = self.JOB_POOL.get(job_id)
            my_job.terminate()

    def get_job_status(self, job_id):
        status = None
        if job_id in self.JOB_POOL:
            my_job = self.JOB_POOL.get(job_id)
            status = my_job.status.value
        return status


class JobManager(BaseJobManager):
    def execute_job(self, target: NetworkFunction, data_model: dict,
                    timeout: int = None, action: ActionType = None,
                    element: str = None):
        return super(JobManager, self).execute_job(JobType.USE_ACTION, target,
                                                   data_model, timeout,
                                                   action=action,
                                                   element=element)


class AnsibleJobManager(BaseJobManager):
    def execute_job(self, target: NetworkFunction, data_model: dict,
                    timeout: int = None, backup_template: str = None,
                    apply_template: str = None, verify_template: str = None,
                    rollback_template: str = None, tags: list = None,
                    extra_vars: dict = None):
        return super().execute_job(JobType.USE_TEMPLATE, target, data_model,
                                   timeout, driver_type=DriverType.ANSIBLE,
                                   backup_template=backup_template,
                                   apply_template=apply_template,
                                   verify_template=verify_template,
                                   rollback_template=rollback_template,
                                   tags=tags,
                                   extra_vars=extra_vars)
