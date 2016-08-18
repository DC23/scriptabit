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
from datetime import datetime
from tzlocal import get_localzone

from .dates import parse_date_utc
from .task import CharacterAttribute, Difficulty, Task


class HabiticaTask(Task):
    """ Defines a Habitica synchronisation task.
    """

    def __init__(self, task_dict=None):
        """ Initialise the task.

        Args:
            task_dict (dict): The Habitica task dictionary, as returned by
                HabiticaService.
        """
        super().__init__()

        if not task_dict:
            task_dict = {'text': 'scriptabit todo'}

        if not isinstance(task_dict, dict):
            raise TypeError(type(task_dict))

        self.__task_dict = task_dict

        # ensure that some required values are defined
        task_dict['type'] = 'todo'

        if 'priority' not in task_dict:
            self.__difficulty = Difficulty.default

        if 'attribute' not in task_dict:
            self.__attribute = CharacterAttribute.default

    @property
    def task_dict(self):
        """ Gets the internal task dictionary. """
        return self.__task_dict

    @property
    def id(self):
        """ Task id """
        return self.__task_dict['_id']

    @property
    def name(self):
        """ Task name """
        return self.__task_dict['text']

    @name.setter
    def name(self, name):
        """ Task name """
        self.__task_dict['text'] = name

    @property
    def description(self):
        """ Task description """
        return self.__task_dict['notes']

    @description.setter
    def description(self, description):
        """ Task description """
        self.__task_dict['notes'] = description

    @property
    def completed(self):
        """ Task completed """
        return self.__task_dict['completed']

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        self.__task_dict['completed'] = completed

    @property
    def difficulty(self):
        """ Task difficulty """
        return self.__difficulty

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        self.__task_dict['priority'] = difficulty.value
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
        self.__task_dict['attribute'] = attribute.value
        self.__attribute = attribute

    @property
    def due_date(self):
        """ The due date if there is one, or None. """
        datestr = self.__task_dict.get('date', None)
        if datestr:
            return parse_date_utc(datestr, milliseconds=True)
        return None

    @due_date.setter
    def due_date(self, due_date):
        """ Sets or clears the due date. """
        if due_date and not isinstance(due_date, datetime):
            raise TypeError
        if due_date:
            self.__task_dict['date'] = \
                due_date.astimezone(get_localzone()).date()
        elif 'date' in self.__task_dict:
            del self.__task_dict['date']

    @property
    def last_modified(self):
        """ The last modified timestamp in UTC. """
        timestamp = self.__task_dict['updatedAt']
        if timestamp:
            return parse_date_utc(timestamp)
