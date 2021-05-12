import time

from networkautomation.common import JobStatus
from networkautomation import job


class JobManager:
    JOB_POOL = {}
    DEFAULT_JOB_TIMEOUT = 3 * 60  # seconds

    def execute_job(self, job_type, target, driver_type=None, templates=None,
                    role=None, action=None, vars=None,
                    timeout=DEFAULT_JOB_TIMEOUT):
        myjob = job.Job(job_type, target, driver_type=driver_type,
                       templates=templates, role=role, action=action,
                       vars=vars)
        if myjob:
            self.JOB_POOL[myjob.id] = myjob
            return myjob.execute(timeout)
        else:
            return False, 'Error: can not init job'

    def register_job(self, job_type, target, driver_type=None, templates=None,
                  role=None, action=None, vars=None):
        myjob = job.Job(job_type, target, driver_type=driver_type,
                       templates=templates, role=role, action=action,
                       vars=vars)
        if myjob:
            self.JOB_POOL[myjob.id] = myjob
            return myjob.id
        else:
            print('Can not init job')
            return None

    def start_job(self, job_id, timeout=DEFAULT_JOB_TIMEOUT):
        myjob = self.JOB_POOL.get(job_id)
        if myjob:
            myjob.execute(timeout)
        else:
            print('Can not find job ', job_id)

    def wait_to_finish_job(self, job_id, timeout=None, auto_terminate=True):
        myjob = self.JOB_POOL.get(job_id)
        timeout_microsec = 0
        if timeout:
            timeout_microsec = timeout*1000000
        begin_time = time.time()
        while myjob.status != JobStatus.FINISHED:
            if (timeout_microsec > 0) \
                    and (time.time() - begin_time >= timeout_microsec):
                if auto_terminate:
                    myjob.terminate()
                break
            else:
                time.sleep(2)

    def terminate_job(self, job_id):
        if job_id in self.JOB_POOL:
            myjob = self.JOB_POOL.get(job_id)
            myjob.terminate()

    def get_job_status(self, job_id):
        status = None
        if job_id in self.JOB_POOL:
            myjob = self.JOB_POOL.get(job_id)
            status = myjob.status.value
        return status
