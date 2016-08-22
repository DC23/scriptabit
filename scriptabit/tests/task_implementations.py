# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
import json
import pytest
import pytz
import requests
import requests_mock
import uuid
from copy import deepcopy
from datetime import datetime
from pkg_resources import resource_filename

from scriptabit import (
    Task,
    Difficulty,
    CharacterAttribute,
    ChecklistItem,
    SyncStatus,
    TaskService,
    TaskMap)


class MockTask(Task):
    def __init__(
            self,
            _id,
            name='',
            description='',
            completed=False,
            difficulty=Difficulty.easy,
            attribute=CharacterAttribute.strength,
            status=SyncStatus.new,
            due_date=None,
            last_modified=None):
        super().__init__()
        self.__id = _id
        self.name = name
        self.description = description
        self.completed = completed
        self.difficulty = difficulty
        self.attribute = attribute
        self.status = status
        self.due_date = due_date
        self.__last_modified = last_modified or datetime.now(tz=pytz.utc)
        self.__checklist = []

    @property
    def id(self):
        """ Task id """
        return self.__id

    @property
    def name(self):
        """ Task name """
        return self.__name

    @name.setter
    def name(self, name):
        """ Task name """
        self.__name = name

    @property
    def description(self):
        """ Task description """
        return self.__description

    @description.setter
    def description(self, description):
        """ Task description """
        self.__description = description

    @property
    def completed(self):
        """ Task completed """
        return self.__completed

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        self.__completed = completed

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

    @property
    def due_date(self):
        """ The due date if there is one, or None. """
        return self.__due_date

    @due_date.setter
    def due_date(self, due_date):
        """ Sets or clears the due date. """
        if due_date and not isinstance(due_date, datetime):
            raise TypeError
        self.__due_date = due_date

    @property
    def last_modified(self):
        """ The last modified timestamp in UTC. """
        return self.__last_modified

    @property
    def checklist(self):
        """ The checklist, or None if there is no checklist."""
        return self.__checklist

    @checklist.setter
    def checklist(self, checklist):
        """ Sets, or clears the checklist. """
        self.__checklist = checklist


class MockTaskService(TaskService):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.persisted_tasks = []

    def get_all_tasks(self):
        """ Get all tasks """
        return self.tasks

    def get_task(self, _id):
        """ Gets a task by id """
        # Quick and nasty sequential search, good enough for testing
        for t in self.tasks:
            if t.id == _id:
                return t
        return None

    def persist_tasks(self, tasks):
        self.persisted_tasks = tasks

    def _create_task(self, src=None):
        return MockTask(_id=uuid.uuid4())
