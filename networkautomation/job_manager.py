import time

from networkautomation.common import JobState
from networkautomation import job


class JobManager:
    JOB_POOL = {}
    DEFAULT_JOB_TIMEOUT = 3 * 60  # seconds

    def execute_job(self, job_type, target, driver_type=None, templates=None,
                    element=None, action=None, extra_vars=None,
                    timeout=DEFAULT_JOB_TIMEOUT):
        my_job = job.Job(job_type, target, driver_type=driver_type,
                         templates=templates, element=element, action=action,
                         extra_vars=extra_vars)
        if my_job:
            self.JOB_POOL[my_job.id] = my_job
            return my_job.execute(timeout)
        else:
            return False, 'Error: can not init job'

    def register_job(self, job_type, target, driver_type=None, templates=None,
                     element=None, action=None, extra_vars=None):
        my_job = job.Job(job_type, target, driver_type=driver_type,
                         templates=templates, element=element, action=action,
                         extra_vars=extra_vars)
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
