# -*- coding: utf-8 -*-
""" Defines an abstract task service.

A task service provides the following features:

    - Query for tasks (including all tasks)
    - Persist a list of tasks
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
from abc import ABCMeta, abstractmethod

from .task import SyncStatus, Task

class TaskService(object):
    """ Defines an abstract Task Service.
    """
     # old-style ABCMeta usage for Python 2.7 compatibility.
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_all_tasks(self):
        """ Get all tasks """
        return NotImplemented

    @abstractmethod
    def get_task(self, id):
        """ Gets a task by id """
        return NotImplemented

    @abstractmethod
    def persist_tasks(self, tasks):
        """ Persists all dirty tasks """
        return NotImplemented

    @abstractmethod
    def _task_factory(self):
        return NotImplemented

    def create(self, src=None):
        """ Creates a new task.

        Args:
            src (Task): The optional data source.

        Returns: Task: The new task.
        """
        # TODO: logging statements
        t = self._task_factory()
        if src:
            t.copy_fields(src, status=SyncStatus.new)
        return t
