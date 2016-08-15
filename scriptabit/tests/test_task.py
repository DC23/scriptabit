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
    TaskMap,
)

from .task_implementations import *


def test_task_service_():
    """Confirm that the abstract base class features work on all supported
    Python versions"""
    task0 = Task('000', name='task 0')
    expected = [task0]
    ts = TestTaskService(expected)
    actual = ts.get_all_tasks()
    assert actual == expected
    assert actual[0].name == task0.name

def test_default_task():
    task = Task()
    assert task.name == ''
    assert task.description == ''
    assert task.id == ''
    assert task.completed == False
    assert task.difficulty == Difficulty.easy
    assert task.attribute == CharacterAttribute.strength
    assert task.dirty == False

def test_invalid_difficulty():
    task = Task()
    with pytest.raises(TypeError):
        task.difficulty = 'really hard'

def test_invalid_attribute():
    task = Task()
    with pytest.raises(TypeError):
        task.attribute = 'dex'

def test_valid_difficulty():
    task = Task()
    task.difficulty = Difficulty.trivial

def test_valid_attribute():
    task = Task()
    task.attribute = CharacterAttribute.intelligence

def test_difficulty_values():
    assert Difficulty.trivial.value == 0.1
    assert Difficulty.easy.value == 1.0
    assert Difficulty.medium.value == 1.5
    assert Difficulty.hard.value == 2.0
