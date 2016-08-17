# -*- coding: utf-8 -*-
""" Implements the Trello synchronisation task service.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from scriptabit import TaskService

from .trello_task import TrelloTask

class TrelloTaskService(TaskService):
    """ Implements the Trello synchronisation task service.
    """
    def __init__(
            self,
            trello_client,
            lists,
            done_lists):
        """ Initialises the Trello synchronisation task service.

        Args:
            trello_client (trello.TrelloClient): The Trello client.
            lists (list): The list of Trello lists to sync from.
            done_lists (list): The list of Trello boards containing
                completed tasks.
        """
        super().__init__()
        self.__tc = trello_client
        self.__lists = lists
        self.__done_lists = done_lists

    @staticmethod
    def __get_tasks_from_lists(lists, force_completed):
        """ Gets all tasks from a list of Trello lists.

        Args:
            lists (list): The Trello lists.
            force_completed (bool): The completion status override.

        Returns:
            list: The list of TrelloTask instances.
        """
        tasks = []
        for l in lists:
            for card in l.list_cards(card_filter='open'):
                # card.fetch()  # force load most card data
                task = TrelloTask(card, force_completed=force_completed)
                tasks.append(task)
        return tasks

    def get_all_tasks(self):
        """ Get all tasks.

        Returns:
            list: The list of tasks
        """
        tasks = self.__get_tasks_from_lists(
            self.__lists,
            force_completed=False)

        tasks.extend(self.__get_tasks_from_lists(
            self.__done_lists,
            force_completed=True))

        return tasks

    def persist_tasks(self, tasks):
        """ Task factory method.

        Allows subclasses to create the appropriate Task type.

        Returns:
            Task: The new task
        """
        raise NotImplementedError

    def _create_task(self, src=None):
        """ Task factory method.

        Args:
            src (Task): The optional data source.

        Returns:
            TrelloTask: A new TrelloTask instance.
        """
        raise NotImplementedError
