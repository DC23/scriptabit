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

# TODO: Implement dry run support if I implement task writing
class TrelloTaskService(TaskService):
    """ Implements the Trello synchronisation task service.
    """
    def __init__(
            self,
            trello_client,
            lists,
            done_lists,
            board_config):
        """ Initialises the Trello synchronisation task service.

        Args:
            trello_client (trello.TrelloClient): The Trello client.
            lists (list): The list of Trello lists to sync from.
            done_lists (list): The list of Trello boards containing
                completed tasks.
            board_config (dict): The dictionary of board configuration data.
        """
        super().__init__()
        self.__tc = trello_client
        self.__lists = lists
        self.__done_lists = done_lists
        self.__board_config = board_config
        self.__current_user = trello_client.get_member('me')

    def __get_tasks_from_lists(self, lists, force_completed):
        """ Gets all tasks from a list of Trello lists.

        Args:
            lists (list): The Trello lists.
            force_completed (bool): The completion status override.

        Returns:
            list: The list of TrelloTask instances.
        """
        tasks = []

        for l in lists:
            board_defaults = self.__board_config[l.board.name]
            for card in l.list_cards(card_filter='open'):

                # Check whether we can use this card or not based on the board
                # settings: all cards or only those assigned to the current user
                use_card = False

                if 'no sync' in [l.name for l in card.labels]:
                    use_card = False
                elif board_defaults.all_cards:
                    use_card = True
                else:
                    card.fetch()  # we need the fetch to get the user ID
                    use_card = self.__current_user.id in card.member_id

                if use_card:
                    task = TrelloTask(
                        card,
                        default_difficulty=board_defaults.difficulty,
                        default_attribute=board_defaults.attribute,
                        force_completed=force_completed)
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
