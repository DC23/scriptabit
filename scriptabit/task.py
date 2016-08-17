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
from datetime import datetime


class Difficulty(Enum):
    """ Implements Task difficulty levels. """
    trivial = 0.1
    easy = 1.0
    medium = 1.5
    hard = 2.0
    default = 1.0

    @staticmethod
    def from_value(value):
        """ Creates an enum instance from the corresponding value. """
        for e in Difficulty:
            if e.value == value:
                return e
        return Difficulty.default


class CharacterAttribute(Enum):
    """ Implements Task character attributes """
    strength = 'str'
    intelligence = 'int'
    constitution = 'con'
    perception = 'per'
    default = 'str'

    @staticmethod
    def from_value(value):
        """ Creates an enum instance from the corresponding value. """
        for e in CharacterAttribute:
            if e.value == value:
                return e
        return CharacterAttribute.default


class SyncStatus(Enum):
    """ Indicates the synchronisation status of the task.
    """
    new = 1
    updated = 2
    deleted = 3
    unchanged = 4


# pylint: disable=no-self-use
class Task(object):
    """ Defines a Habitica task data transfer object.

    Essentially this is the common features of a task as found in many task
    management applications. If a task from a particular service can be mapped
    to this class, then moving tasks between services becomes easier.

    Attributes:
        id (str): The task ID.
        name (str): The task name.
        due_date (datetime): The due date in UTC
        description (str): The description.
        completed (bool): Completion/checked status
        difficulty (Difficulty): task difficulty.
        attribute (CharacterAttribute): habitica character attribute of the task
        status (SyncStatus): Synchronisation status flag.
    """
    # TODO: define and add checklists

    def __init__(self):
        """ Initialise the task.
        """
        super().__init__()
        self.__status = SyncStatus.new

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

    @property
    def status(self):
        """ Task status """
        return self.__status

    @status.setter
    def status(self, status):
        """ Task status """
        if not isinstance(status, SyncStatus):
            raise TypeError
        self.__status = status

    @property
    def due_date(self):
        """ The due date in UTC if there is one, or None. """
        raise NotImplementedError

    @due_date.setter
    def due_date(self, due_date):
        """ Sets or clears the due date. """
        if not isinstance(due_date, datetime):
            raise TypeError
        raise NotImplementedError

    def copy_fields(self, src, status=SyncStatus.updated):
        """ Copies fields from src.

        Args:
            src (Task): the source task
            status (SyncStatus): the status to set

        Returns:
            Task: self
        """
        self.name = src.name
        self.description = src.description
        self.completed = src.completed
        self.difficulty = src.difficulty
        self.attribute = src.attribute
        self.due_date = src.due_date
        self.status = status
        return self
# pylint: enable=no-self-use
