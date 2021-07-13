import multiprocessing
import os
import time
import traceback

import psutil
import networkautomation.drivers.driver_manager as driver_manager
import networkautomation.utils as utils
from networkautomation import data_model
from networkautomation.common import *
from networkautomation.network_function import NetworkFunction


def kill(pid):
    try:
        os.kill(pid, 15)
        time.sleep(1)
    except Exception as ex:
        print('Killed process maybe exited: ' + str(ex))


def run_single_process(driver, state, target, job_type, data_model, child_conn,
                       **kwargs):
    try:
        error = driver.execute(state, target, job_type, data_model, **kwargs)
        if error:
            child_conn.send(str(error))
        else:
            child_conn.send(TaskResult.TASK_OK)
        child_conn.close()
    except Exception as err:
        print("Task raised: %s" % err)
        print(traceback.format_exc())
        child_conn.send(str(err))
        child_conn.close()


class TaskResult:
    TASK_OK = 'OK'
    TASK_TIMEOUT = 'Timeout'
    TASK_DRIVER_NOT_FOUND = 'Driver is not found'

    def __init__(self, name, err):
        self.name = name
        self.err = err

    def __repr__(self) -> str:
        return 'Task ' + self.name + ': ' + self.err


class Job:
    def __init__(self, job_type: JobType, target: NetworkFunction,
                 model: dict, **kwargs):
        self.id = utils.gen_uuid()
        self.job_type = job_type
        self.target = target
        self.error = []
        self.driver = None
        self.pid = None
        self.data_model = model
        self.state = JobState.INIT
        self.kwargs = kwargs
        self.driver_type = self.kwargs.get('driver_type')
        # data_model.DataModel.validate_data(self.data_model)
        self.driver = driver_manager.get_driver(self.driver_type,
                                                self.target,
                                                self.kwargs.get('element'))

    def execute(self, timeout):
        if not self.driver:
            self.error.append(TaskResult(self.state.value,
                                         TaskResult.TASK_DRIVER_NOT_FOUND))
            return False, str(self.error)
        if self.run_task(JobState.BACKUP, timeout) \
                and self.run_task(JobState.APPLY, timeout) \
                and self.run_task(JobState.VERIFY, timeout):
            self.state = JobState.FINISHED
            return True, None
        return False, str(self.error)

    def recover(self, state, timeout):
        print('Start to recover')
        if state == JobState.APPLY or state == JobState.VERIFY:
            self.run_task(JobState.ROLLBACK, timeout)

    def run_task(self, state, timeout):
        self.state = state
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=run_single_process,
                                    kwargs=self.kwargs,
                                    args=(self.driver, self.state.value,
                                          self.target, self.job_type,
                                          self.data_model, child_conn))
        p.start()
        self.pid = p.pid
        p.join(timeout=timeout)
        if p.exitcode is None:
            # Timeout then, terminate process
            print("Task is timeout after " + str(timeout))
            self.error.append(TaskResult(self.state.value,
                                         TaskResult.TASK_TIMEOUT + ' after ' +
                                         str(timeout) + ' seconds'))
            self.terminate()
        else:
            res = parent_conn.recv()
            if res == TaskResult.TASK_OK:
                # Task is done and successful
                return True
            else:
                # Task is done but fail
                print("Task failed: %s" % res)
                self.error.append(TaskResult(self.state.value, res))
        self.recover(self.state, timeout)
        return False

    def terminate(self):
        current_process = psutil.Process(self.pid)
        children = current_process.children(recursive=True)
        for child in reversed(children):
            kill(child.pid)
        kill(self.pid)
