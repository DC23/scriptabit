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
from pkg_resources import resource_filename

from scriptabit import (
    Task,
    Difficulty,
    CharacterAttribute,
    TaskService,
    TaskMapping,
)


class TestTaskService(TaskService):
    def __init__(self, tasks):
        super().__init__()
        self.tasks = tasks

    def get_all_tasks(self):
        """ Get all tasks """
        return self.tasks

    def persist_tasks(self, tasks):
        pass
