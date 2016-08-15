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

from bidict import (
    KeyDuplicationError,
    ValueDuplicationError,
    KeyAndValueDuplicationError)
from tempfile import NamedTemporaryFile
from scriptabit import SyncStatus, TaskSync, Task, TaskMap

from .task_implementations import TestTaskService


def test_new_tasks():
    src_tasks = [Task(id=i) for i in range(2)]
    dst_tasks = []
    src = TestTaskService(src_tasks)
    dst = TestTaskService(dst_tasks)
    map = TaskMap()
    sync = TaskSync(src, dst, map)
    sync.synchronise()

    assert len(dst.persisted_tasks) == 2
    assert isinstance(dst.persisted_tasks[0], Task)
    assert dst.persisted_tasks[0].status == SyncStatus.new
