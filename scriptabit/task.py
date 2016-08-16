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
# from abc import ABCMeta, abstractmethod
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


class SyncStatus(Enum):
    """ Indicates the synchronisation status of the task.
    """
    new = 1
    updated = 2
    deleted = 3
    unchanged = 4


class Task(object):
    """ Defines a Habitica task data transfer object.

    Essentially this is the common features of a task as found in many task
    management applications. If a task from a particular service can be mapped
    to this class, then moving tasks between services becomes easier.

    Attributes:
        id (str): The task ID.
    """
    # TODO: logging statements
    # TODO: define and add checklists
    # TODO: define due date

    def __init__(
            self,
            _id,
            name='',
            description='',
            completed=False,
            difficulty=Difficulty.easy,
            attribute=CharacterAttribute.strength,
            status=SyncStatus.new):
        """ Initialise the task.

        Args:
            _id (str): The task ID
            name (str): The task name.
            description (str): A longer description
            completed (bool): Indicates the completion status of the task.
            difficulty (Difficulty): The task difficulty.
            attribute (CharacterAttribute): Character attribute of the task.
            status (SyncStatus): Sync status hint for the TaskService.
        """
        super().__init__()
        self.__id = _id
        self.name = name
        self.description = description
        self.completed = completed
        self.difficulty = difficulty
        self.attribute = attribute
        self.status = status

    @property
    def id(self):
        """ Task id """
        return self.__id

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

    @property
    def status(self):
        """ Task status """
        raise NotImplementedError

    @status.setter
    def status(self, status):
        """ Task status """
        raise NotImplementedError

    def copy_fields(self, src, status=SyncStatus.updated):
        """ Copies fields from src.

        Args:
            src (Task): the source task
            status (SyncStatus): the status to set

        Returns: Task: self
        """
        self.name = src.name
        self.description = src.description
        self.completed = src.completed
        self.difficulty = src.difficulty
        self.attribute = src.attribute
        self.status = status
        return self
