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

    - No mapping found:

        - new task
        - if task completed, check if last modified date is newer than last sync
          date

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
from datetime import datetime

import pytz
from tzlocal import get_localzone

from .task import SyncStatus


# pylint: disable=too-few-public-methods
class TaskSync(object):
    """ Provides synchronisation between two task services.
    """

    class Stats(object):
        """ Simple sync stats """
        def __init__(self):
            """ Initialise the stats """
            self.skipped = 0
            self.created = 0
            self.updated = 0
            self.completed = 0
            self.deleted = 0
            self.errors = 0
            self.duration = None

        def __str__(self):
            """ Get a nicely formatted stats string """
            return (
                '\tTasks skipped: {0}\n' +
                '\tTasks created: {1}\n' +
                '\tTasks updated: {2}\n' +
                '\tTasks deleted: {3}\n' +
                '\tTasks completed: {4}\n' +
                '\tTasks errored: {6}\n' +
                '\tSync duration: {5}\n').format(
                    self.skipped, self.created, self.updated, self.deleted,
                    self.completed, self.duration, self.errors)

        @property
        def total_changed(self):
            """ Get the total number of changed tasks. """
            return self.created +\
                self.updated +\
                self.completed +\
                self.deleted

    def __init__(
            self,
            src_service,
            dst_service,
            task_map,
            last_sync=None,
            sync_description=True):
        """ Initialise the TaskSync instance.

        Args:
            src_service (TaskService): The TaskService for source tasks.
            dst_service (TaskService): The TaskService for destination tasks.
            task_map (TaskMap): The TaskMap.
            last_sync (datetime): The last known synchronisation datetime (UTC).
            sync_description (bool): Controls whether the task description will
                be synchronised.
        """
        self.__src_service = src_service
        self.__dst_service = dst_service
        self.__map = task_map
        self.__last_sync = last_sync or datetime.min.replace(tzinfo=pytz.utc)
        self.__src_tasks = None
        self.__dst_tasks = None
        self.__src_index = None
        self.__dst_index = None
        self.__sync_description = sync_description
        self.__stats = TaskSync.Stats()

    def __create_new_dst(self, src):
        """ Creates and maps a new destination task.

        Args:
            src (Task): source task

        Returns:
            Task: The new destination task
        """
        # factory method as we don't know the concrete task type
        dst = self.__dst_service.create(src)
        if not self.__sync_description:
            dst.description = ''
        self.__map.map(src, dst)
        return dst

    def __get_src_by_id(self, _id):
        """ Looks up a cached source task by ID """
        return self.__src_index.get(_id, None)

    def __get_dst_by_id(self, _id):
        """ Looks up a cached destination task by ID """
        return self.__dst_index.get(_id, None)

    def __get_task_data(self):
        """ Gets, caches, and indexes task data from the source and destination
        services.
        """
        logging.getLogger(__name__).debug('Fetching source tasks')
        self.__src_tasks = self.__src_service.get_all_tasks()

        logging.getLogger(__name__).debug('Fetching destination tasks')
        self.__dst_tasks = self.__dst_service.get_all_tasks()

        self.__src_index = {s.id:s for s in self.__src_tasks}
        self.__dst_index = {d.id:d for d in self.__dst_tasks}

    def __handle_destination_found(self, src, dst):
        """ Handle the case where a pair of mapped tasks exist.

        Args:
            src (Task): the source task
            dst (Task): the destination task
        """
        if src.last_modified < self.__last_sync:
            # It seems that I don't care about unchanged messages even with
            # debug level logging enabled.
            # logging.getLogger(__name__).debug(
                # 'Unchanged: %s', src.name)
            self.__stats.skipped += 1
            return

        if src.completed:
            logging.getLogger(__name__).info(
                'Completing: %s', src.name)
            self.__stats.completed += 1
        else:
            logging.getLogger(__name__).info(
                'Updating: %s', src.name)
            self.__stats.updated += 1
        dst.copy_fields(src, status=SyncStatus.updated)
        if not self.__sync_description:
            dst.description = ''

    def __handle_destination_missing(self, src):
        """ Handle the case where a mapped destination task cannot be found.

        Args:
            src (Task): the source task
        """
        if not src.completed:
            # recreate if src is not complete,
            logging.getLogger(__name__).info(
                'Recreating: %s',
                src.name)
            self.__map.unmap(src.id)
            self.__dst_tasks.append(self.__create_new_dst(src))
            self.__stats.created += 1
        else:
            # otherwise ignore
            logging.getLogger(__name__).debug(
                'Ignoring deleted/completed destination task: %s',
                src.name)
            self.__stats.skipped += 1

    def __handle_new_task(self, src):
        """ Handle a new source task.

        Args:
            src (Task): the source task
        """
        create = False
        if src.completed and src.last_modified >= self.__last_sync:
            logging.getLogger(__name__).info(
                'Creating (completed): %s',
                src.name)
            create = True
        elif not src.completed:
            logging.getLogger(__name__).info(
                'Creating: %s',
                src.name)
            create = True

        if create:
            self.__dst_tasks.append(self.__create_new_dst(src))
            self.__stats.created += 1

    def __handle_deleted_source_task(self, src_id, dst):
        """ Handle the case where a mapped destination task exists but the
        source task cannot be located.

        Args:
            src_id (str): the source task ID
            dst (Task): the destination task
        """
        logging.getLogger(__name__).debug(
            'Deleting: %s --> %s', src_id, dst.name)
        dst.status = SyncStatus.deleted
        self.__stats.deleted += 1

    def __clean_orphan_task_mappings(self):
        """ Removes task mappings where neither the source or destination
        tasks exist.
        """
        # this may be bad for large maps, but we can't delete entries
        # while iterating
        all_src_keys = list(self.__map.get_all_src_keys())
        for src_key in all_src_keys:
            dst_key = self.__map.get_dst_id(src_key)
            if not self.__get_src_by_id(src_key) \
                and not self.__get_dst_by_id(dst_key):
                logging.getLogger(__name__).debug(
                    'Found orphan relationship: %s --> %s',
                    src_key,
                    dst_key)
                self.__map.unmap(src_key)

    def synchronise(
            self,
            clean_orphans=False):
        """ Synchronise the source service with the destination.
        The task_map will be updated.

        Args:
            clean_orphans (bool): If True, mappings for tasks that exist in
                neither the source or destination are deleted.

        Returns:
            TaskSync.Stats: Summary statistics of the sync.
        """
        start_sync = datetime.now(tz=pytz.utc)

        self.__get_task_data()

        logging.getLogger(__name__).info(
            'Starting sync. Last sync at %s',
            self.last_sync.astimezone(get_localzone()))

        # reset the stats
        self.__stats = TaskSync.Stats()

        # source task checks
        for src in self.__src_tasks:
            try:
                dst_id = self.__map.try_get_dst_id(src.id)
                if dst_id:
                    dst = self.__get_dst_by_id(dst_id)
                    if dst:
                        self.__handle_destination_found(src, dst)
                    else:
                        self.__handle_destination_missing(src)
                else:
                    self.__handle_new_task(src)
            except Exception as e:
                self.__stats.errors += 1
                logging.getLogger(__name__).warning(
                    "Error syncing task '%s':\n%s",
                    src.name,
                    e,
                    exc_info=True)

        # destination task checks. Only need to look for cases involving missing
        # source tasks. All other sync conditions can be handled during the
        # source task loop (above).
        for dst in self.__dst_tasks:
            try:
                src_id = self.__map.try_get_src_id(dst.id)
                if src_id and not self.__get_src_by_id(src_id):
                    self.__handle_deleted_source_task(src_id, dst)
            except Exception as e:
                self.__stats.errors += 1
                logging.getLogger(__name__).warning(
                    "Error syncing task '%s':\n%s",
                    dst.name,
                    e,
                    exc_info=True)

        # check for orphans: mappings that have neither a src or dst task
        if clean_orphans:
            self.__clean_orphan_task_mappings()

        try:
            self.__dst_service.persist_tasks(self.__dst_tasks)
        except Exception as e:
            self.__stats.errors += 1
            logging.getLogger(__name__).warning(
                'Error writing task changes.\n%s',
                e,
                exc_info=True)

        end_sync = datetime.now(tz=pytz.utc)
        self.__stats.duration = end_sync - start_sync
        self.__last_sync = end_sync

        logging.getLogger(__name__).info('Sync complete.')
        logging.getLogger(__name__).info(self.__stats)

        return self.__stats

    @property
    def last_sync(self):
        """ Gets the last synchronisation datestamp.

        Returns:
            datetime: The last synchronisation time.
        """
        return self.__last_sync
# pylint: enable=too-few-public-methods
