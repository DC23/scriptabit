# -*- coding: utf-8 -*-
""" Provides synchronisation between two task services.

Basic algorithm
+++++++++++++++

- Build list of candidate tasks from source and destination services
- Index the candidate tasks for lookup by ID
- Get the existing list of source to destination task mappings
- Check all source tasks

    - Mapping exists, destination task found:

        - update destination

    - Mapping exists, destination task not found:

        - recreate destination
        - alternatively, could delete source task

    - No mapping found: new task

- Check all destination tasks for which mapped source tasks can't be found:

    - assume deleted and flag destination as 'deleted'

- Check for orphan mappings: both source and destination not found

    - delete mapping

- **Not implemented**: persist source tasks
- Persist destination tasks

"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

from .task import SyncStatus


# pylint: disable=too-few-public-methods
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
        self.__src_service = src_service
        self.__dst_service = dst_service
        self.__map = task_map

    def __create_new_dst(self, src):
        """ Creates and maps a new destination task.

        Args:
            src (Task): source task

        Returns:
            Task: The new destination task
        """
        # factory method as we don't know the concrete task type
        dst = self.__dst_service.create(src)
        self.__map.map(src, dst)
        return dst

    def synchronise(self, clean_orphans=False, recreate_completed_tasks=False):
        """ Synchronise the source service with the destination.
        The task_map will be updated.

        Args:
            clean_orphans (bool): If True, mappings for tasks that exist in
                neither the source or destination are deleted.
            recreate_completed_tasks (bool): If True, completed source tasks
                that are missing from the destination will be recreated.
        """
        src_tasks = self.__src_service.get_all_tasks()
        dst_tasks = self.__dst_service.get_all_tasks()

        src_index = {s.id:s for s in src_tasks}
        dst_index = {d.id:d for d in dst_tasks}

        def get_src_by_id(_id):
            """ Looks up a cached source task by ID """
            return src_index.get(_id, None)

        def get_dst_by_id(_id):
            """ Looks up a cached destination task by ID """
            return dst_index.get(_id, None)

        # run through the source tasks, checking for existing mappings
        for src in src_tasks:
            dst_id = self.__map.try_get_dst_id(src.id)
            if dst_id:
                dst = get_dst_by_id(dst_id)
                if dst:
                    # dst found, so this is an existing mapping
                    logging.getLogger(__name__).debug(
                        'task mapping found, updating: %s --> %s',
                        src.id, dst_id)
                    dst.copy_fields(src, status=SyncStatus.updated)
                else:
                    # dst expected but not found, assume deleted.
                    # TODO: Should we recreate? Or delete back to source?
                    if recreate_completed_tasks or not src.completed:
                        logging.getLogger(__name__).debug(
                            'dst task not found, recreating: %s --> %s',
                            src.id, dst_id)
                        self.__map.unmap(src.id)
                        dst_tasks.append(self.__create_new_dst(src))
            else:
                # mapping not found, so create new task
                # factory method as we don't know the concrete task type
                logging.getLogger(__name__).debug(
                    'Found new task: %s: %s', src.id, src.name)
                dst_tasks.append(self.__create_new_dst(src))

        # check for deleted tasks: mappings where we have dst but not src
        for dst in dst_tasks:
            src_id = self.__map.try_get_src_id(dst.id)
            if not get_src_by_id(src_id):
                # source deleted for existing mapping
                logging.getLogger(__name__).debug(
                    'Found deleted task: %s --> %s', src_id, dst.id)
                dst.status = SyncStatus.deleted

        # check for orphans: mappings that have neither a src or dst task
        if clean_orphans:
            # this may be bad for large maps, but we can't delete entries
            # while iterating
            all_src_keys = list(self.__map.get_all_src_keys())
            for src_key in all_src_keys:
                dst_key = self.__map.get_dst_id(src_key)
                if not get_src_by_id(src_key) and not get_dst_by_id(dst_key):
                    logging.getLogger(__name__).debug(
                        'Found orphan task map: %s --> %s', src_key, dst_key)
                    self.__map.unmap(src_key)

        # TODO: should this be optional?
        self.__dst_service.persist_tasks(dst_tasks)

# pylint: enable=too-few-public-methods
