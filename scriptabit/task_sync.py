# -*- coding: utf-8 -*-
""" Provides synchronisation between two task services.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from .task import SyncStatus, Task
from .task_map import TaskMap
from .task_service import TaskService


class TaskSync(object):
    """ Provides synchronisation between two task services.
    """

    def __init__(self, src_service, dst_service, task_map):
        """ Initialise the TaskSync instance.

        Args:
            src_service (TaskService): The TaskService for source tasks.
            dst_service (TaskService): The TaskService for destination tasks.
            task_map (TaskMap): The TaskMap.
        """
        self.src_service = src_service
        self.dst_service = dst_service
        self.map = task_map

    def __create_new_dst(self, src):
        """ Creates and maps a new destination task.
        Args:
            src (Task): source task

        Returns: Task: The new destination task
        """
        # factory method as we don't know the concrete task type
        dst = self.dst_service.create(src)
        # TODO: should this be set by the factory method?
        dst.status = SyncStatus.new
        self.map.map(src, dst)
        return dst

    def synchronise(self):
        """ Synchronise the source service with the destination.
        The task_map will be updated.
        """

        src_tasks = self.src_service.get_all_tasks()
        dst_tasks = self.dst_service.get_all_tasks()

        # run through the source tasks, checking for existing mappings
        for src in src_tasks:
            dst_id = self.map.try_get_dst_id(src)
            if dst_id:
                dst = self.__get_by_id(dst_tasks, dst_id)
                if dst:
                    # dst found, so this is an existing mapping
                    # TODO: task copy
                    dst.status = SyncStatus.updated
                else:
                    # dst expected but not found, assume deleted.
                    # TODO: Should we recreate? Or delete back to source?
                    dst_tasks.append(self.__create_new_dst(src))
            else:
                # mapping not found, so create new task
                # factory method as we don't know the concrete task type
                dst_tasks.append(self.__create_new_dst(src))

        # TODO: check for orphans: mappings that have neither a src or dst task
        # TODO: check for deleted tasks: mapping where we have dst but not src

        self.dst_service.persist_tasks(dst_tasks)
