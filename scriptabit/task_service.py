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
        """ Get all tasks. """
        raise NotImplementedError

    def get_task(self, _id):
        """ Gets a task by id.

        Args:
            _id (str): The task ID to get.

        Returns: Task: The task if it exists, otherwise None.
        """
        raise NotImplementedError

    def persist_tasks(self, tasks):
        """ Persists the tasks.

        New and existing tasks will be upserted. Tasks flagged for deletion
        will be deleted.

        Args: tasks: The collection of tasks to persist.
        """
        raise NotImplementedError

    def _create_task(self):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.
        """
        raise NotImplementedError

    # pylint correctly detects that _task_factory returns NotImplemented, but
    # it fails to detect that the method is marked abstract, so the error is
    # spurious.
    #pylint: disable=no-member
    def create(self, src=None):
        """ Creates a new task.

        Args:
            src (Task): The optional data source.

        Returns: Task: The new task.
        """
        t = self._create_task()
        if src:
            t.copy_fields(src, status=SyncStatus.new)
        return t
