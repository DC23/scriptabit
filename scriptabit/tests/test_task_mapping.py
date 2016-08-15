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
from scriptabit import Task, TaskMapping


class TestTaskMapping(object):

    def setup(self):
        self.tm = TaskMapping()
        self.src = Task(id='1')
        self.dst = Task(id='a')
        self.missing = Task(id='blah')

    def test_persist_task_mapping(self):
        expected = TaskMapping()
        tasks = [Task(id=i) for i in range(4)]
        expected.map(tasks[0], tasks[1])
        expected.map(tasks[2], tasks[3])
        filename = NamedTemporaryFile(suffix='.pickle')
        expected.persist(filename.name)
        actual = TaskMapping(filename.name)

        assert actual.get_dst_id(tasks[0]) == tasks[1].id
        assert actual.get_dst_id(tasks[2]) == tasks[3].id
        assert actual.get_src_id(tasks[1]) == tasks[0].id
        assert actual.get_src_id(tasks[3]) == tasks[2].id

    def test_duplicate_src(self):
        s = Task('1')
        d = Task('a')
        dd = Task('aa')
        self.tm.map(s, d)
        with pytest.raises(KeyDuplicationError):
            self.tm.map(s, dd)

    def test_duplicate_dst(self):
        src2 = Task(id='9')
        self.tm.map(self.src, self.dst)
        with pytest.raises(ValueDuplicationError):
            self.tm.map(src2, self.dst)

    def test_duplicate_src_dst(self):
        tasks = [Task(id=i) for i in range(4)]
        self.tm.map(tasks[0], tasks[1])
        self.tm.map(tasks[2], tasks[3])
        with pytest.raises(KeyAndValueDuplicationError):
            # both src and dst are already mapped to something
            self.tm.map(tasks[0], tasks[3])

    def test_valid_forward(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.get_dst_id(self.src) == self.dst.id

    def test_invalid_forward(self):
        with pytest.raises(KeyError):
            self.tm.get_dst_id(self.missing)

    def test_valid_reverse(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.get_src_id(self.dst) == self.src.id

    def test_invalid_reverse(self):
        with pytest.raises(KeyError):
            self.tm.get_src_id(self.missing)

    def test_valid_forward_try_get(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.try_get_dst_id(self.src) == self.dst.id

    def test_invalid_forward_try_get(self):
        assert not self.tm.try_get_dst_id(self.missing)

    def test_valid_reverse_try_get(self):
        self.tm.map(self.src, self.dst)
        assert self.tm.try_get_src_id(self.dst) == self.src.id

    def test_invalid_reverse_try_get(self):
        assert not self.tm.try_get_src_id(self.missing)
