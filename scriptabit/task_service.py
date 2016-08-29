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

from .task import SyncStatus


class TaskService(object):
    """ Defines an abstract Task Service.
    """
    def get_all_tasks(self):
        """ Get all tasks.

        Returns:
            list: The list of tasks
        """
        raise NotImplementedError

    def persist_tasks(self, tasks):
        """ Persists the tasks.

        Args:
            tasks (list): The collection of tasks to persist.
        """
        raise NotImplementedError

    def _create_task(self, src=None):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.

        Args:
            src (Task): The optional data source.

        Returns:
            Task: The new task
        """
        raise NotImplementedError

    def create(self, src=None):
        """ Creates a new task.

        Args:
            src (Task): The optional data source.

        Returns:
            Task: The new task.
        """
        t = self._create_task(src)
        if src:
            t.copy_fields(src, status=SyncStatus.new)
        return t
