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
    HabiticaTask,
    Difficulty,
    CharacterAttribute,
    SyncStatus)

from .fake_data import get_fake_task


def test_id():
    d = get_fake_task(_id='432')[0]
    task = HabiticaTask(d)
    assert d['_id'] == '432'
    assert task.id == '432'

def test_create_default():
    task = HabiticaTask()
    assert task
    assert task.name == 'scriptabit todo'
    assert task.difficulty == Difficulty.default
    assert task.attribute == CharacterAttribute.default

def test_invalid_difficulty():
    task = HabiticaTask(get_fake_task()[0])
    with pytest.raises(TypeError):
        task.difficulty = 'really hard'

def test_existing_difficulty():
    task = get_fake_task()[0]
    expected = Difficulty.hard
    task['priority'] = expected.value
    ht = HabiticaTask(task)
    assert ht.difficulty == expected

def test_invalid_attribute():
    task = HabiticaTask(get_fake_task()[0])
    with pytest.raises(TypeError):
        task.attribute = 'dex'

def test_valid_difficulty():
    task = HabiticaTask(get_fake_task()[0])
    task.difficulty = Difficulty.trivial
    assert task.difficulty == Difficulty.trivial

def test_valid_attribute():
    task = HabiticaTask(get_fake_task()[0])
    task.attribute = CharacterAttribute.intelligence
    assert task.attribute == CharacterAttribute.intelligence

def test_existing_attribute():
    task = get_fake_task()[0]
    expected = CharacterAttribute.constitution
    task['attribute'] = expected.value
    ht = HabiticaTask(task)
    assert ht.attribute == expected

def test_id_readonly():
    task = HabiticaTask(get_fake_task()[0])
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

    d = get_fake_task(_id=_id, text=name, notes=description, completed=completed)[0]
    a = HabiticaTask(d)

    a.difficulty = difficulty
    a.status = status
    a.attribute = attribute

    assert a.id == _id
    assert a.name == name
    assert a.description == description
    assert a.completed == completed
    assert a.difficulty == difficulty
    assert a.attribute == attribute
    assert a.status == status
