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

from pkg_resources import resource_filename
from random import randint, choice

from bidict import (
    KeyDuplicationError,
    ValueDuplicationError,
    KeyAndValueDuplicationError)
from tempfile import NamedTemporaryFile
from scriptabit import (
    SyncStatus,
    TaskSync,
    Task,
    TaskMap,
    Difficulty,
    CharacterAttribute)

from .task_implementations import TestTaskService, TestTask


difficulties = (
    Difficulty.trivial,
    Difficulty.easy,
    Difficulty.medium,
    Difficulty.hard)

attributes = (
    CharacterAttribute.strength,
    CharacterAttribute.intelligence,
    CharacterAttribute.constitution,
    CharacterAttribute.perception)

def random_task():
    t = TestTask(id=uuid.uuid4())
    t.name = uuid.uuid1()
    t.description = 'blah blah tired blah coffee'
    t.completed = choice((True, False))
    t.difficulty = difficulties[randint(0,len(difficulties)-1)]
    t.attribute = attributes[randint(0,len(attributes)-1)]
    return t

def test_new_tasks():
    src_tasks = [random_task() for x in range(3)]
    dst_tasks = []
    src = TestTaskService(src_tasks)
    dst = TestTaskService(dst_tasks)
    map = TaskMap()
    sync = TaskSync(src, dst, map)
    sync.synchronise()

    assert len(dst.persisted_tasks) == len(src_tasks)
    for d in dst.persisted_tasks:
        assert d.status == SyncStatus.new
        assert d in dst_tasks
        assert map.try_get_src_id(d)

    for s in src.get_all_tasks():
        assert map.try_get_dst_id(s)

