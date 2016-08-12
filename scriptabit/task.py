# -*- coding: utf-8 -*-
""" Defines an abstract task.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

class Task(object):
    """ Defines a Habitica task data transfer object.

    Essentially this is the common features of a task as found in many task
    management applications. If a task from a particular service can be mapped
    to this class, then moving tasks between services becomes easier.

    Attributes:
        name (str): The task name.
        description (str): A longer description
        completed (bool): Indicates the completion status of the task.
        difficulty (str): One of 'trivial', 'easy', 'medium', 'hard'.
    """
    # TODO: define and add checklists
    # TODO: what other attributes should I include? ID? Last modified date?

    def __init__(self):
        """ Initialise the task.
        """
        super().__init__()
        self.name = ''
        self.description = ''
        self.completed = False
        self.__difficulty = 'easy'

    @property
    def difficulty(self):
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        if difficulty not in ('trivial', 'easy', 'medium', 'hard'):
            raise ValueError('difficulty not valid')
        self.__difficulty = difficulty
