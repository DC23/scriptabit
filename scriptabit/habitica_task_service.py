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
import uuid

from .habitica_service import HabiticaTaskTypes
from .habitica_task import HabiticaTask
from .task import SyncStatus
from .task_service import TaskService


class HabiticaTaskService(TaskService):
    """ Implements the Habitica synchronisation task service.
    """
    def __init__(self, hs, dry_run=False, tags=None):
        """ Initialises the Habitica synchronisation task service.

        Args:
            hs (HabiticaService): The Habitica Service.
            dry_run (bool): Indicates a dry run.
            tags (list): The list of tags to be applied to synchronised tasks.
        """
        super().__init__()
        self.__hs = hs
        self.__dry_run = dry_run
        self.__task_tags = self.__hs.create_tags(tags) if tags else None

    @property
    def dry_run(self):
        """ Returns the dry run status. """
        return self.__dry_run

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
        if not self.dry_run:
            for task in tasks:
                td = task.task_dict
                if task.completed:
                    # We need to update the task first, as scoring a todo
                    # does not update the data, and the task may have
                    # changed upstream in ways that affect the Habitica
                    # score for completing it.
                    self.__update_task(task)
                    self.__hs.score_task(td)
                elif task.status in (SyncStatus.updated, SyncStatus.new):
                    # new tasks have already been created in _create_task,
                    # so we just need an update.
                    self.__update_task(task)
                elif task.status == SyncStatus.deleted:
                    self.__hs.delete_task(td)

    def __update_task(self, task):
        """ Updates a task. This is required as checklists require tedious
        handling.

        Args:
            task (scriptabit.HabiticaTask): The task to update.
        """
        assert not self.dry_run
        td = task.task_dict

        # delete existing checklist items
        for i in task.existing_checklist_items:
            self.__hs.delete_checklist_item(td['_id'], i['id'])

        # recreate the new set of checklist items
        for i in task.new_checklist_items:
            self.__hs.create_checklist_item(td['_id'], i)
            # do I need to score checked items separately?

        # update the rest of the task
        self.__hs.update_task(td)

    def _create_task(self, src=None):
        """ Task factory method.

        Args:
            src (Task): The optional data source.

        Returns:
            HabiticaTask: A new HabiticaTask instance.
        """

        new_task_dict = {
            'text': src.name,
            'tags': [t['id'] for t in self.__task_tags]
        }

        if self.dry_run:
            # create a fake random ID for the dry run
            new_task_dict['_id'] = uuid.uuid4(),
        else:
            new_task_dict = self.__hs.create_task(new_task_dict)

        return HabiticaTask(new_task_dict)
