import multiprocessing
import os
import time
import traceback

import psutil

import networkautomation.drivers.driver_manager as driver_manager
import networkautomation.utils as utils
from networkautomation.common import *
from networkautomation.network_function import NetworkFunction


class Job:
    def __init__(self, job_type: JobType, target: NetworkFunction,
                 driver_type: DriverType = None, templates = None, id=None,
                 role=None, action: ActionType = None, vars=None):
        self.id = id or utils.gen_uuid()
        self.job_type = job_type
        self.target = target
        self.templates = templates
        self.state = JobStatus.INIT
        self.driver_type = driver_type
        self.error = ''
        self.role = role
        self.action = action
        self.driver = None
        self.vars = vars
        self.pid = None
        if driver_type:
            self.driver = driver_manager.get_driver_from_name(
                driver_type.value, self.target)


    def get_driver(self, state):
        driver = self.driver
        if not driver:
            driver = driver_manager.get_driver_from_state(self.role,
                                                          state.value,
                                                          self.target)
        return driver

    def run_single_process(self, driver, state, target, templates, vars,
                           child_conn):
        try:
            driver.execute(state, target, templates, vars)
        except Exception as err:
            print("Task raised: %s" % err)
            print(traceback.format_exc())
            child_conn.send(str(err))
            child_conn.close()
            exit(-1)

    def execute(self, timeout):
        if self.run_task(JobStatus.BACKUP, timeout) \
            and self.run_task(JobStatus.APPLY, timeout) \
                and self.run_task(JobStatus.VERIFY, timeout):
                    self.status = JobStatus.FINISHED
                    return True, ''
        return False, self.error

    def recover(self, state, timeout):
        print('Start to recover')
        if state == JobStatus.APPLY or state == JobStatus.VERIFY:
            self.run_task(JobStatus.ROLLBACK, timeout)

    def run_task(self, state, timeout):
        self.state = state
        driver = self.get_driver(self.state)
        if not driver:
            print("Bypass task %s" % self.state)
            return True
        parent_conn, child_conn = multiprocessing.Pipe()
        p = multiprocessing.Process(target=self.run_single_process,
                    args=(driver, self.state.value, self.target,
                          self.templates, self.vars, child_conn))
        p.start()
        self.pid = p.pid
        p.join(timeout=timeout)
        if p.exitcode == 0:
            # Task is done
            return True
        else:
            if p.exitcode == None:
                # Timeout then, terminate process
                print("Task is timeout after " + str(timeout))
                self.error = self.error + "Timeout| "
                self.terminate()
            else:
                err = parent_conn.recv()
                print("Task got exception: %s" % err)
                self.error = self.error + err + "| "
            self.recover(self.state, timeout)
            return False

    def kill(self, pid):
        try:
            os.kill(pid, 15)
            time.sleep(1)
        except Exception as ex:
            print('Killed process maybe exited: ' + str(ex))

    def terminate(self):
        current_process = psutil.Process(self.pid)
        children = current_process.children(recursive=True)
        for child in reversed(children):
            self.kill(child.pid)
        self.kill(self.pid)
