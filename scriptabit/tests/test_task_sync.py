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

from datetime import datetime, timedelta
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

from .task_implementations import MockTaskService, MockTask


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

def random_task(completed=False, last_modified=None):
    t = MockTask(_id=uuid.uuid4(), last_modified=last_modified)
    t.name = uuid.uuid1()
    t.description = 'blah blah tired blah coffee'
    t.completed = completed
    t.difficulty = difficulties[randint(0,len(difficulties)-1)]
    t.attribute = attributes[randint(0,len(attributes)-1)]
    t.status = SyncStatus.unchanged
    return t

def test_new_tasks():
    src_tasks = [random_task() for x in range(3)]
    dst_tasks = []
    src = MockTaskService(src_tasks)
    dst = MockTaskService(dst_tasks)
    map = TaskMap()
    sync = TaskSync(src, dst, map)
    sync.synchronise()

    assert len(dst.persisted_tasks) == len(src_tasks)
    for d in dst.persisted_tasks:
        assert d.status == SyncStatus.new
        assert d in dst_tasks
        assert map.try_get_src_id(d.id)

    for s in src.get_all_tasks():
        dst_id = map.try_get_dst_id(s.id)
        assert dst_id
        d = dst.get_task(dst_id)
        assert s.name == d.name
        assert s.description == d.description
        assert s.completed == d.completed
        assert s.difficulty == d.difficulty
        assert s.attribute == d.attribute

def test_new_tasks_are_mapped():
    src_tasks = [random_task()]
    dst_tasks = []
    src = MockTaskService(src_tasks)
    dst = MockTaskService(dst_tasks)
    map = TaskMap()
    sync = TaskSync(src, dst, map)

    # preconditions
    assert len(map.get_all_src_keys()) == 0

    sync.synchronise()

    assert len(map.get_all_src_keys()) == 1
    assert src_tasks[0].id in map.get_all_src_keys()
    assert map.get_dst_id(src_tasks[0].id) == dst_tasks[0].id

def test_missing_mapped_destination_tasks_src_complete():
    """ Tests expected behaviours on mapped tasks that are missing in
    the destination.
    """
    src = random_task()
    src.completed = True
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)

    dst = random_task()
    dst_tasks = []
    dst_svc = MockTaskService(dst_tasks)

    map = TaskMap()

    # create the pre-existing mapping
    map.map(src, dst)

    # preconditions
    assert len(map.get_all_src_keys()) == 1
    assert map.get_dst_id(src.id) == dst.id
    assert map.get_src_id(dst.id) == src.id

    TaskSync(src_svc, dst_svc, map).synchronise()

    assert len(dst_svc.tasks) == 0

def test_missing_mapped_destination_tasks_src_not_complete():
    """ Tests expected behaviours on mapped tasks that are missing in
    the destination.
    """
    src = random_task()
    src.completed = False
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)

    dst = random_task()
    dst_tasks = []
    dst_svc = MockTaskService(dst_tasks)

    map = TaskMap()

    # create the pre-existing mapping
    map.map(src, dst)

    # preconditions
    assert len(map.get_all_src_keys()) == 1
    assert map.get_dst_id(src.id) == dst.id
    assert map.get_src_id(dst.id) == src.id

    TaskSync(src_svc, dst_svc, map).synchronise()

    assert dst.id != dst_svc.tasks[0].id
    assert len(map.get_all_src_keys()) == 1, "should still be just one mapping"
    assert not map.try_get_src_id(dst.id), "old dst should be unmapped"
    assert map.get_dst_id(src.id) != dst.id, "src should be mapped to something else"
    assert dst_svc.tasks[0].status == SyncStatus.new, "should be flagged as a new task"
    assert len(dst_svc.tasks) == 1

def test_existing_tasks_are_updated():
    src = random_task()
    src.difficulty = Difficulty.hard
    src.attribute = CharacterAttribute.strength
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)
    dst = random_task()
    dst.description = 'something different'
    dst.difficulty = Difficulty.medium
    dst.attribute = CharacterAttribute.constitution
    dst_tasks = [dst]
    dst_svc = MockTaskService(dst_tasks)

    # precondition tests
    assert src.id != dst.id
    assert src.status == SyncStatus.unchanged
    assert dst.name != src.name
    assert dst.attribute != src.attribute
    assert dst.difficulty != src.difficulty
    assert dst.status == SyncStatus.unchanged
    assert dst.description != src.description
    map = TaskMap()
    map.map(src, dst)

    sync = TaskSync(src_svc, dst_svc, map)
    sync.synchronise()

    assert len(dst_svc.persisted_tasks) == 1
    actual = dst_svc.persisted_tasks[0]
    assert actual.id == dst.id, "id not changed"
    assert actual.id != src.id, "id not changed"
    assert actual.name == src.name
    assert actual.attribute == src.attribute
    assert actual.difficulty == src.difficulty
    assert actual.completed == src.completed
    assert actual.status == SyncStatus.updated
    assert actual.description == src.description
    assert actual.completed == src.completed

def test_old_existing_tasks_are_not_updated():
    last_sync = datetime(2016, 8, 15, tzinfo=pytz.utc)
    # make the src modified date older than the last sync
    src_mod_date = last_sync - timedelta(days=2)
    dst_mod_date = last_sync + timedelta(minutes=1)
    src = random_task(last_modified=src_mod_date)
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)

    dst = random_task(last_modified=dst_mod_date)
    dst_tasks = [dst]
    dst_svc = MockTaskService(dst_tasks)

    map = TaskMap()
    map.map(src, dst)

    # preconditions
    assert dst.status == SyncStatus.unchanged

    TaskSync(src_svc, dst_svc, map, last_sync=last_sync).synchronise()

    assert len(dst_svc.persisted_tasks) == 1
    assert dst.status == SyncStatus.unchanged

def test_new_existing_tasks_are_updated():
    last_sync = datetime(2016, 8, 15, tzinfo=pytz.utc)
    # make the src modified date newer than the last sync
    src_mod_date = last_sync + timedelta(minutes=2)
    dst_mod_date = last_sync + timedelta(minutes=1)
    src = random_task(last_modified=src_mod_date)
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)

    dst = random_task(last_modified=dst_mod_date)
    dst_tasks = [dst]
    dst_svc = MockTaskService(dst_tasks)

    map = TaskMap()
    map.map(src, dst)

    # preconditions
    assert dst.status == SyncStatus.unchanged

    TaskSync(src_svc, dst_svc, map).synchronise()

    assert len(dst_svc.persisted_tasks) == 1
    assert dst.status == SyncStatus.updated

def test_deleted_src_tasks():
    src_tasks = []
    dst = random_task()
    dst_tasks = [dst]
    ss = MockTaskService(src_tasks)
    ds = MockTaskService(dst_tasks)
    map = TaskMap()

    # we need to create a mapping between a src task and dst, but leave
    # the source task out of the source service
    src = random_task()
    map.map(src, dst)

    sync = TaskSync(ss, ds, map)

    # preconditions
    assert len(ss.tasks) == 0
    assert len(ds.tasks) == 1
    assert dst.status == SyncStatus.unchanged

    sync.synchronise()

    # the task list lengths should not be changed
    assert len(ss.tasks) == 0
    assert len(ds.tasks) == 1

    # dst should now be flagged as deleted
    assert dst.status == SyncStatus.deleted

def test_remove_orphan_mappings():
    src_tasks = [random_task()]
    dst_tasks = []
    ss = MockTaskService(src_tasks)
    ds = MockTaskService(dst_tasks)
    map = TaskMap()

    # add a few task mappings that won't exist in either source or destination
    map.map(random_task(), random_task())
    map.map(random_task(), random_task())
    map.map(random_task(), random_task())

    TaskSync(ss, ds, map).synchronise(clean_orphans=True)

    # We now expect just one mapping for the new src task
    all_mappings = map.get_all_src_keys()
    assert len(all_mappings) == 1
    assert map.get_dst_id(src_tasks[0].id)

def test_new_completed_tasks():
    src = random_task(completed=True)
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)
    dst_tasks = []
    dst_svc = MockTaskService(dst_tasks)
    map = TaskMap()
    TaskSync(src_svc, dst_svc, map).synchronise()

    assert len(dst_svc.tasks) == 1
    assert dst_svc.tasks[0].completed
    assert dst_svc.tasks[0].status == SyncStatus.new

def test_new_completed_tasks_are_updated_when_last_mod_newer_than_last_sync():
    last_sync = datetime(2016, 8, 15, tzinfo=pytz.utc)
    src_mod_date = last_sync + timedelta(hours=2)
    src = random_task(completed=True, last_modified=src_mod_date)
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)
    dst_svc = MockTaskService([])

    TaskSync(src_svc, dst_svc, TaskMap(), last_sync=last_sync).synchronise()

    assert len(dst_svc.persisted_tasks) == 1
    assert dst_svc.tasks[0].status == SyncStatus.new

def test_new_completed_tasks_are_not_updated_when_last_mod_older_than_last_sync():
    last_sync = datetime(2016, 8, 15, tzinfo=pytz.utc)
    src = random_task(
        completed=True,
        last_modified=last_sync - timedelta(days=2))
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)
    dst_svc = MockTaskService([])

    TaskSync(src_svc, dst_svc, TaskMap(), last_sync=last_sync).synchronise()

    assert len(dst_svc.persisted_tasks) == 0

def test_completion_of_existing_mapped_tasks():
    src = random_task(completed=True)
    src_tasks = [src]
    src_svc = MockTaskService(src_tasks)

    dst = random_task()
    # make dst the same in all but the completed flag
    dst.copy_fields(dst)
    dst.completed = False
    dst_tasks = [dst]
    dst_svc = MockTaskService(dst_tasks)

    map = TaskMap()
    map.map(src, dst)

    assert not dst_svc.tasks[0].completed

    TaskSync(src_svc, dst_svc, map).synchronise()

    assert len(dst_svc.tasks) == 1
    assert dst_svc.tasks[0].completed
    assert dst_svc.tasks[0].status == SyncStatus.updated
