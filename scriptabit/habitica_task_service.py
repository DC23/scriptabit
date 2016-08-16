# -*- coding: utf-8 -*-
""" Defines an abstract task service.

A task service provides the following features:

    - Query for tasks (including all tasks)
    - Create a new task
    - Persist a list of tasks
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from .habitica_service import HabiticaTaskTypes
from .habitica_task import HabiticaTask
from .task import SyncStatus


class TaskService(object):
    """ Implements the Habitica synchronisation task service.
    """
    def __init__(self, hs):
        """ Initialises the Habitica synchronisation task service.

        Args:
            hs (HabiticaService): The Habitica Service.
        """
        super().__init__()
        self.__hs = hs

    def get_all_tasks(self):
        """ Get all tasks. """
        raw_tasks = self.__hs.get_tasks(task_type=HabiticaTaskTypes.todos)
        tasks = [HabiticaTask(rt) for rt in raw_tasks]
        for t in tasks:
            t.status = SyncStatus.unchanged
        return tasks

    def persist_tasks(self, tasks):
        """ Persists the tasks.

        New and existing tasks will be upserted. Tasks flagged for deletion
        will be deleted.

        Args: tasks: The collection of tasks to persist.
        """
        for task in tasks:
            # TODO: new tasks can be created with a single API call. I should do that
            if task.status in (SyncStatus.updated, SyncStatus.new):
                self.__hs.upsert_task(task)
            elif task.status == SyncStatus.deleted:
                self.__hs.delete_task(task)

    def _create_task(self):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.
        """
        return HabiticaTask()
