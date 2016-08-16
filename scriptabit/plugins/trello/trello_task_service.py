# -*- coding: utf-8 -*-
""" Implements the Trello synchronisation task service.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from scriptabit import SyncStatus, TaskService

from .trello_task import TrelloTask

class TrelloTaskService(TaskService):
    """ Implements the Trello synchronisation task service.
    """
    def __init__(self):
        """ Initialises the Trello synchronisation task service.

        Args:
        """
        super().__init__()
        raise NotImplementedError

    def get_all_tasks(self):
        """ Get all tasks.

        Returns:
            list: The list of tasks
        """
        raise NotImplementedError

    def persist_tasks(self, tasks):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.

        Returns:
            Task: The new task
        """
        raise NotImplementedError

    def _create_task(self):
        """ Task factory method.

        Returns:
            TrelloTask: A new TrelloTask instance.
        """
        return TrelloTask()
