# -*- coding: utf-8 -*-
""" Implements a Trello synchronisation task.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from scriptabit import CharacterAttribute, Difficulty, Task


class TrelloTask(Task):
    """ Defines a Trello synchronisation task.
    """

    def __init__(self, card, force_completed=False):
        """ Initialise the task.

        Args:
            card (Trello.Card): The underlying Trello card.
            force_completed (bool): If True, the task will report as completed
                even if card.closed is False.
        """
        super().__init__()
        self.__card = card
        self.__force_completed = force_completed

    @property
    def id(self):
        """ Task id """
        return self.__card.id

    @property
    def name(self):
        """ Task name """
        return self.__card.name

    @name.setter
    def name(self, name):
        """ Task name """
        self.__card.set_name(name)

    @property
    def description(self):
        """ Task description """
        return self.__card.description

    @description.setter
    def description(self, description):
        """ Task description """
        self.__card.set_description(description)

    @property
    def completed(self):
        """ Task completed """
        return self.__force_completed or self.__card.closed

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        self.__card.set_closed(completed)

    @property
    def difficulty(self):
        """ Task difficulty """
        # TODO: parse difficulty from labels
        return Difficulty.easy

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        raise NotImplementedError
        # TODO: apply a label to set the difficulty

    @property
    def attribute(self):
        """ Task character attribute """
        # TODO: parse from label
        return CharacterAttribute.strength

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        if not isinstance(attribute, CharacterAttribute):
            raise TypeError
        raise NotImplementedError
        # TODO: apply a label
