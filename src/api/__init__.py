"""
APIģ�����
�汾: 1.0.0
"""
from .exceptions import APIError, TaskNotFound, InvalidTaskData
from .task_api import TaskAPI
from .stats_api import StatsAPI

__all__ = [
    'TaskAPI',
    'StatsAPI',
    'APIError',
    'TaskNotFound',
    'InvalidTaskData'
]

__version__ = '1.0.0'