from enum import Enum


class JobState(Enum):
    INIT = 'INIT'
    APPLY = 'APPLY'
    BACKUP = 'BACKUP'
    ROLLBACK = 'ROLLBACK'
    VERIFY = 'VERIFY'
    FINISHED = 'FINISHED'


class JobType(Enum):
    PROVISIONING = 'provisioning'
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
