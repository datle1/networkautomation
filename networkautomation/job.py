import multiprocessing
import os
import time
import traceback

import psutil
import networkautomation.drivers.driver_manager as driver_manager
import networkautomation.utils as utils
from networkautomation.common import *
from networkautomation.network_function import NetworkFunction

TASK_OK = 'OK'


def kill(pid):
    try:
        os.kill(pid, 15)
        time.sleep(1)
    except Exception as ex:
        print('Killed process maybe exited: ' + str(ex))


def run_single_process(driver, state, target, templates, extra_vars,
                       child_conn):
    try:
        error = driver.execute(state, target, templates, extra_vars)
        if error:
            child_conn.send(str(error))
        else:
            child_conn.send(TASK_OK)
        child_conn.close()
    except Exception as err:
        print("Task raised: %s" % err)
        print(traceback.format_exc())
        child_conn.send(str(err))
        child_conn.close()


class Job:
    def __init__(self, job_type: JobType, target: NetworkFunction,
                 driver_type: DriverType = None, templates=None, job_id=None,
                 element=None, action: ActionType = None, extra_vars=None):
        self.id = job_id or utils.gen_uuid()
        self.job_type = job_type
        self.target = target
        self.templates = templates
        self.state = JobState.INIT
        self.driver_type = driver_type
        self.error = ''
        self.element = element
        self.action = action
        self.driver = None
        self.vars = extra_vars
        self.pid = None
        if driver_type:
            self.driver = driver_manager.get_driver_from_name(
                driver_type.value, self.target)

    def get_driver(self, state):
        driver = self.driver
        if not driver:
            driver = driver_manager.get_driver_from_state(self.element,
                                                          state.value,
                                                          self.target)
        return driver

    def execute(self, timeout):
        if self.run_task(JobState.BACKUP, timeout) \
                and self.run_task(JobState.APPLY, timeout) \
                and self.run_task(JobState.VERIFY, timeout):
            self.state = JobState.FINISHED
            return True, None
        return False, self.error

    def recover(self, state, timeout):
        print('Start to recover')
        if state == JobState.APPLY or state == JobState.VERIFY:
            self.run_task(JobState.ROLLBACK, timeout)

    def run_task(self, state, timeout):
        self.state = state
        driver = self.get_driver(self.state)
        if not driver:
            print("Bypass task %s" % self.state)
            return True
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=run_single_process,
                                    args=(driver, self.state.value,
                                          self.target, self.templates,
                                          self.vars, child_conn))
        p.start()
        self.pid = p.pid
        p.join(timeout=timeout)
        if p.exitcode is None:
            # Timeout then, terminate process
            print("Task is timeout after " + str(timeout))
            self.error = self.error + "Task " + self.state.value \
                                    + " got timeout| "
            self.terminate()
        else:
            res = parent_conn.recv()
            if res == TASK_OK:
                # Task is done and successful
                return True
            else:
                # Task is done but fail
                print("Task failed: %s" % res)
                self.error = self.error + res + "| "
        self.recover(self.state, timeout)
        return False

    def terminate(self):
        current_process = psutil.Process(self.pid)
        children = current_process.children(recursive=True)
        for child in reversed(children):
            kill(child.pid)
        kill(self.pid)
