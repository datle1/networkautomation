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


def run_single_process(driver, state, target, templates, action, element,
                       input_vars, child_conn):
    try:
        error = driver.execute(state, target, templates, action, element,
            input_vars)
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
                 driver_type: DriverType = None, templates=None, job_id=None,
                 action: ActionType = None,  element=None, input_vars=None):
        self.id = job_id or utils.gen_uuid()
        self.job_type = job_type
        self.target = target
        self.templates = templates
        self.state = JobState.INIT
        self.driver_type = driver_type
        self.error = []
        self.element = element
        self.action = action
        self.driver = None
        self.vars = input_vars
        self.pid = None

        # if self.vars:
        #     data_model.DataModel.validate_data(self.vars)

        self.driver = driver_manager.get_driver(self.driver_type,
            self.target, self.element)

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
                                    args=(self.driver, self.state.value,
                                          self.target, self.templates,
                                          self.action, self.element,
                                          self.vars, child_conn))
        p.start()
        self.pid = p.pid
        p.join(timeout=timeout)
        if p.exitcode is None:
            # Timeout then, terminate process
            print("Task is timeout after " + str(timeout))
            self.error.append(TaskResult(self.state.value,
                              TaskResult.TASK_TIMEOUT))
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
