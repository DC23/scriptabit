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
        self.map.map(src, dst)
        return dst

    def synchronise(self):
        """ Synchronise the source service with the destination.
        The task_map will be updated.
        """

        src_tasks = self.src_service.get_all_tasks()
        dst_tasks = self.dst_service.get_all_tasks()

        src_index = { s.id:s for s in src_tasks }
        dst_index = { d.id:d for d in dst_tasks }

        def get_src_by_id(id):
            """ Looks up a cached source task by ID """
            return src_index.get(id, None)

        def get_dst_by_id(id):
            """ Looks up a cached destination task by ID """
            return dst_index.get(id, None)

        # run through the source tasks, checking for existing mappings
        for src in src_tasks:
            dst_id = self.map.try_get_dst_id(src)
            if dst_id:
                dst = get_dst_by_id(dst_id)
                if dst:
                    # dst found, so this is an existing mapping
                    dst.copy_fields(src, status=SyncStatus.updated)
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
