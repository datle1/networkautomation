from enum import Enum


class JobStatus(Enum):
    INIT = 'INIT'
    APPLY = 'APPLY'
    BACKUP = 'BACKUP'
    ROLLBACK = 'ROLLBACK'
    VERIFY = 'VERIFY'
    FINISHED = 'FINISHED'


class JobType(Enum):
    PROVISIONING = 'provisioing'
    CONFIGURATION = 'configuration'


class DriverType(Enum):
    ANSIBLE = 'ansible'
    REST = 'rest'
    CLI = 'cli'
    NETCONF = 'netconf'


class ActionType(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'
