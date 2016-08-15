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
from enum import Enum


class Difficulty(Enum):
    """ Implements Task difficulty levels. """
    trivial = 0.1
    easy = 1.0
    medium = 1.5
    hard = 2.0


class CharacterAttribute(Enum):
    """ Implements Task character attributes """
    strength = 'str'
    intelligence = 'int'
    constitution = 'con'
    perception = 'per'


class Task(object):
    """ Defines a Habitica task data transfer object.

    Essentially this is the common features of a task as found in many task
    management applications. If a task from a particular service can be mapped
    to this class, then moving tasks between services becomes easier.

    Attributes:
        name (str): The task name.
        description (str): A longer description
        id (str): The task ID
        completed (bool): Indicates the completion status of the task.
        difficulty (Difficulty): The task difficulty.
        attribute (CharacterAttribute): Character attribute of the task.
        dirty (bool): Indicates that the task is dirty and requires persistence.
            Note that the dirty flag is **not** set automatically when
            attributes are modified. Clients must set this value manually as
            required.
    """
    # TODO: define and add checklists
    # TODO: define due date

    def __init__(
        self,
        id='',
        name=''):
        """ Initialise the task.

        Args:
            id (str): The task ID
            name (str): The task name.
            description (str): A longer description
        """
        super().__init__()
        self.id = id
        self.name = name
        self.description = ''
        self.completed = False
        self.__difficulty = Difficulty.easy
        self.__attribute = CharacterAttribute.strength
        self.dirty = False

    @property
    def difficulty(self):
        """ Task difficulty """
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        self.__difficulty = difficulty

    @property
    def attribute(self):
        """ Task character attribute """
        return self.__attribute

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        if not isinstance(attribute, CharacterAttribute):
            raise TypeError
        self.__attribute = attribute
