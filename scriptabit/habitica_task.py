# -*- coding: utf-8 -*-
""" Implements a Habitica synchronisation task.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

from .task import Task


class HabiticaTask(Task):
    """ Defines a Habitica synchronisation task.
    """
    def __init__(self, task_dict):
        """ Initialise the task.

        Args:
            task_dict (dict): The Habitica task dictionary, as returned by
                HabiticaService.
        """
        super().__init__(_id=task_dict['_id'])
        self.__task_dict = task_dict

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        super().difficulty = difficulty
        self.__task_dict['priority'] = difficulty.value

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        super().attribute = attribute
        self.__task_dict['attribute'] == attribute.value

    # def name(self, name):
        # """ Task name """
        # super().name = name
