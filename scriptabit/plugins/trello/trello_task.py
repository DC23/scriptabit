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

    def __init__(self):
        """ Initialise the task.

        Args:
        """
        super().__init__()

    @property
    def id(self):
        """ Task id """
        raise NotImplementedError

    @property
    def name(self):
        """ Task name """
        raise NotImplementedError

    @name.setter
    def name(self, name):
        """ Task name """
        raise NotImplementedError

    @property
    def description(self):
        """ Task description """
        raise NotImplementedError

    @description.setter
    def description(self, description):
        """ Task description """
        raise NotImplementedError

    @property
    def completed(self):
        """ Task completed """
        raise NotImplementedError

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        raise NotImplementedError

    @property
    def difficulty(self):
        """ Task difficulty """
        raise NotImplementedError

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        raise NotImplementedError

    @property
    def attribute(self):
        """ Task character attribute """
        raise NotImplementedError

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        if not isinstance(attribute, CharacterAttribute):
            raise TypeError
        raise NotImplementedError
