from networkautomation import network_function, job_manager, common

if __name__ == '__main__':
    target = network_function.NetworkFunction('firewall',
        'fortinet',
        'fortios',
        '7.1',
        {'user': 'admin', 'password': 'admin'},
        '10.10.10.11')
    job_mgmt = job_manager.JobManager()
    result, error = job_mgmt.execute_job(common.JobType.CONFIGURATION,
                                         target, role='vlan',
                                         action=common.ActionType.CREATE)
    if result==True:
        print("Rest job is successful")
    else:
        print("Rest job is failed. Reason: " + error)