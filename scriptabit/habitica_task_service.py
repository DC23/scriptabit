# -*- coding: utf-8 -*-
""" Implements the Habitica synchronisation task service.
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
from .task_service import TaskService


class HabiticaTaskService(TaskService):
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
        """ Get all tasks.

        Returns:
            list: The list of tasks
        """
        raw_tasks = self.__hs.get_tasks(task_type=HabiticaTaskTypes.todos)
        tasks = [HabiticaTask(rt) for rt in raw_tasks]
        for t in tasks:
            t.status = SyncStatus.unchanged
        return tasks

    def persist_tasks(self, tasks):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.

        Returns:
            Task: The new task
        """
        for task in tasks:
            td = task.task_dict
            if task.completed:
                self.__hs.score_task(td)
            elif task.status in (SyncStatus.updated, SyncStatus.new):
                # new tasks have already been created in _create_task,
                # so we just need an update.
                self.__hs.update_task(td)
            elif task.status == SyncStatus.deleted:
                self.__hs.delete_task(td)

    def _create_task(self, src=None):
        """ Task factory method.

        Args:
            src (Task): The optional data source.

        Returns:
            HabiticaTask: A new HabiticaTask instance.
        """

        new_task_dict = self.__hs.create_task({'text': src.name})
        return HabiticaTask(new_task_dict)
