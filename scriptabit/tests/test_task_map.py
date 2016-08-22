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
from scriptabit import Task, TaskMap

from .task_implementations import *


class TestTaskMap(object):

    def setup(self):
        self.tm = TaskMap()
        self.src = MockTask(_id='1')
        self.dst = MockTask(_id='a')
        self.missing = MockTask(_id='blah')

    def test_create_when_file_doesnt_exist(self):
        tmpfile = NamedTemporaryFile(suffix='.pickle')
        name = tmpfile.name
        tmpfile.close()
        tm = TaskMap(name)
        assert tm

    def test_persist_task_mapping(self):
        expected = TaskMap()
        tasks = [MockTask(_id=i) for i in range(4)]
        expected.map(tasks[0], tasks[1])
        expected.map(tasks[2], tasks[3])
        filename = NamedTemporaryFile(suffix='.pickle')
        expected.persist(filename.name)
        actual = TaskMap(filename.name)

        assert actual.get_dst_id(tasks[0].id) == tasks[1].id
        assert actual.get_dst_id(tasks[2].id) == tasks[3].id
        assert actual.get_src_id(tasks[1].id) == tasks[0].id
        assert actual.get_src_id(tasks[3].id) == tasks[2].id

    def test_duplicate_src(self):
        s = MockTask('1')
        d = MockTask('a')
        dd = MockTask('aa')
        self.tm.map(s, d)
        with pytest.raises(KeyDuplicationError):
            self.tm.map(s, dd)

    def test_duplicate_dst(self):
        src2 = MockTask(_id='9')
        self.tm.map(self.src, self.dst)
        with pytest.raises(ValueDuplicationError):
            self.tm.map(src2, self.dst)

    def test_duplicate_src_dst(self):
        tasks = [MockTask(_id=i) for i in range(4)]
        self.tm.map(tasks[0], tasks[1])
        self.tm.map(tasks[2], tasks[3])
        with pytest.raises(KeyAndValueDuplicationError):
            # both src and dst are already mapped to something
            self.tm.map(tasks[0], tasks[3])

    def test_valid_forward(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.get_dst_id(self.src.id) == self.dst.id

    def test_invalid_forward(self):
        with pytest.raises(KeyError):
            self.tm.get_dst_id(self.missing)

    def test_valid_reverse(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.get_src_id(self.dst.id) == self.src.id

    def test_invalid_reverse(self):
        with pytest.raises(KeyError):
            self.tm.get_src_id(self.missing.id)

    def test_valid_forward_try_get(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.try_get_dst_id(self.src.id) == self.dst.id

    def test_invalid_forward_try_get(self):
        assert not self.tm.try_get_dst_id(self.missing.id)

    def test_valid_reverse_try_get(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.try_get_src_id(self.dst.id) == self.src.id

    def test_invalid_reverse_try_get(self):
        assert not self.tm.try_get_src_id(self.missing.id)

    def test_get_all_src_keys(self):
        src_keys = (1,2,3,4)
        src_tasks = [MockTask(_id=i) for i in src_keys]
        dst_tasks = [MockTask(_id=i+20) for i in range(4)]
        map = TaskMap()
        for s,d in zip(src_tasks, dst_tasks):
            map.map(s,d)

        for actual in map.get_all_src_keys():
            assert actual in src_keys

    def test_get_all_dst_keys(self):
        src_tasks = [MockTask(_id=i+20) for i in range(4)]
        dst_keys = (1,2,3,4)
        dst_tasks = [MockTask(_id=i) for i in dst_keys]
        map = TaskMap()
        for s,d in zip(src_tasks, dst_tasks):
            map.map(s,d)

        for actual in map.get_all_dst_keys():
            assert actual in dst_keys

    def test_delete_mapping(self):
        self.tm.map(self.src, self.dst)
        self.tm.unmap(self.src.id)
        assert not self.tm.try_get_dst_id(self.src.id)
        assert not self.tm.try_get_src_id(self.dst.id)
