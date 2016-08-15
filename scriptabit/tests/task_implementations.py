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
import requests
import requests_mock
import uuid
from copy import deepcopy
from pkg_resources import resource_filename

from scriptabit import (
    Task,
    Difficulty,
    CharacterAttribute,
    SyncStatus,
    TaskService,
    TaskMap)


class TestTask(Task):
    def __init__(
        self,
        id,
        name=''):
        super().__init__(id, name)


class TestTaskService(TaskService):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks
        self.persisted_tasks = []

    def get_all_tasks(self):
        """ Get all tasks """
        return self.tasks

    def get_task(self, id):
        """ Gets a task by id """
        # Quick and nasty sequential search, good enough for these small tests
        for t in self.tasks:
            if t.id == id:
                return t
        return None

    def persist_tasks(self, tasks):
        self.persisted_tasks = tasks

    def create(self, src):
        t = TestTask(id=uuid.uuid4()).copy_fields(src)
        return t
