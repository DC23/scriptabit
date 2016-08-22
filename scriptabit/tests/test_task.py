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
import pytz
import time
from pkg_resources import resource_filename
from datetime import datetime

from scriptabit import (
    Task,
    Difficulty,
    CharacterAttribute,
    ChecklistItem,
    TaskService,
    TaskMap)

from .task_implementations import *


def test_task_service():
    """Confirm that the abstract base class features work on all supported
    Python versions"""
    task0 = MockTask(_id='000', name='task 0')
    expected = [task0]
    ts = MockTaskService(expected)
    actual = ts.get_all_tasks()
    assert actual == expected
    assert actual[0].name == task0.name

def test_default_task():
    task = MockTask(_id='432')
    assert task.id == '432'

def test_invalid_difficulty():
    task = MockTask(_id='439')
    with pytest.raises(TypeError):
        task.difficulty = 'really hard'

def test_invalid_attribute():
    task = MockTask(_id='99')
    with pytest.raises(TypeError):
        task.attribute = 'dex'

def test_valid_difficulty():
    task = MockTask(_id='fakjsd')
    task.difficulty = Difficulty.trivial

def test_valid_attribute():
    task = MockTask(_id='34kid0')
    task.attribute = CharacterAttribute.intelligence

def test_difficulty_values():
    assert Difficulty.trivial.value == 0.1
    assert Difficulty.easy.value == 1.0
    assert Difficulty.medium.value == 1.5
    assert Difficulty.hard.value == 2.0

def test_id_readonly():
    task = MockTask(_id='34kid0')
    with pytest.raises(AttributeError):
        task.id = 'aeai239'

def test_init():
    _id = '111'
    name = 'a task'
    description = 'something'
    completed = True
    difficulty = Difficulty.hard
    attribute = CharacterAttribute.intelligence
    status = SyncStatus.updated

    a = MockTask(
        _id, name=name, description=description, completed=completed,
        difficulty=difficulty, attribute=attribute, status=status)

    assert a.id == _id
    assert a.name == name
    assert a.description == description
    assert a.completed == completed
    assert a.difficulty == difficulty
    assert a.attribute == attribute
    assert a.status == status

def test_copy_fields():
    _id = '111'
    name = 'a task'
    description = 'something'
    completed = True
    difficulty = Difficulty.hard
    attribute = CharacterAttribute.intelligence
    status = SyncStatus.updated
    due_date = datetime(2016, 7, 27, 6, 41, 34, 391000, tzinfo=pytz.utc)
    checklist = [
        ChecklistItem('item 1', False),
        ChecklistItem('item 2', True),
        ChecklistItem('item 3', False)]

    a = MockTask(
        _id, name=name, description=description, completed=completed,
        difficulty=difficulty, attribute=attribute, status=status,
        due_date=due_date)
    a.checklist = checklist
    b = MockTask('222')

    # preconditions
    assert a.id != b.id
    assert a.name != b.name
    assert a.description != b.description
    assert a.completed != b.completed
    assert a.difficulty != b.difficulty
    assert a.attribute != b.attribute
    assert a.status != b.status
    assert a.due_date != b.due_date
    assert a.checklist == checklist
    assert not b.checklist

    b.copy_fields(a)

    # postconditions
    assert a.id != b.id
    assert a.name == b.name
    assert a.description == b.description
    assert a.completed == b.completed
    assert a.difficulty == b.difficulty
    assert a.attribute == b.attribute
    assert a.status == b.status
    assert a.due_date == b.due_date
    assert a.checklist == b.checklist
