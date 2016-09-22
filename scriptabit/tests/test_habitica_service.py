# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
import pytest
import requests
import requests_mock
from pkg_resources import resource_filename

from scriptabit.errors import *
from scriptabit.habitica_service import HabiticaService

from .fake_data import *


class TestHabiticaService(object):

    hs = None

    @classmethod
    def setup_class(cls):
        cls.hs = HabiticaService(
            {},
            'https://habitica.com/api/v3/')

    def test_server_status_up(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/status',
                  text='{"data": {"status": "up"}}')
            assert self.hs.is_server_up() is True

    def test_server_status_down(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/status',
                  text='{"data": {"status": "down"}}')
            assert self.hs.is_server_up() is False

    def test_server_status_request_fails(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/status',
                  text='Failure',
                  status_code=requests.codes.no_response)
            assert self.hs.is_server_up() is False

    def test_get_stats_request_fails(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text='Not OK',
                  status_code=requests.codes.server_error)
            with pytest.raises(requests.HTTPError):
                self.hs.get_stats()

    def test_get_stats(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user', text=get_fake_stats()[1])
            stats = self.hs.get_stats()

            assert stats['con'] == 10
            assert stats['int'] == 11
            assert stats['per'] == 12
            assert stats['str'] == 13
            assert stats['hp'] == 47.21
            assert stats['lvl'] == 4
            assert stats['exp'] == 34
            assert stats['toNextLevel'] == 180

    def test_set_hp(self):
        with requests_mock.mock() as m:
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=10)[1])
            new_hp = self.hs.set_hp(10)

            assert new_hp == 10

    def test_set_hp_too_high(self):
        with (pytest.raises(ArgumentOutOfRangeError)):
            self.hs.set_hp(51)

    def test_set_hp_too_low(self):
        with (pytest.raises(ArgumentOutOfRangeError)):
            self.hs.set_hp(-1)

    def test_set_mp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=30)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=16.5)[1])
            new_mp = self.hs.set_mp(16.5)

            assert new_mp == 16.5

    def test_set_mp_too_low(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(maxMP=60)[1])
            with (pytest.raises(ArgumentOutOfRangeError)):
                self.hs.set_mp(-1)

    def test_set_xp(self):
        with requests_mock.mock() as m:
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=168, toNextLevel=180)[1])
            new_exp = self.hs.set_exp(168)
            assert new_exp == 168

    def test_set_xp_too_low(self):
        with (pytest.raises(ArgumentOutOfRangeError)):
            self.hs.set_exp(-1)

    def test_set_gp(self):
        with requests_mock.mock() as m:
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=997.7)[1])
            new_gp = self.hs.set_gp(997.7)
            assert new_gp == 997.7

    def test_set_gp_less_than_zero(self):
        with (pytest.raises(ArgumentOutOfRangeError)):
            self.hs.set_gp(-1)

    def test_set_gp_to_zero(self):
        with requests_mock.mock() as m:
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=0)[1])
            new_gp = self.hs.set_gp(0)
            assert new_gp == 0

    def test_upsert_without_id_or_alias(self):
        with (pytest.raises(ValueError)):
            self.hs.upsert_task({})

    def test_upsert_new_task_created_alias(self):
        # Don't test the data, just that the expected API functions are called
        task = get_fake_task(alias='alias')
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/tasks/alias',
                  status_code=requests.codes.not_found)
            m.post('https://habitica.com/api/v3/tasks/user',
                  text=task[1])
            self.hs.upsert_task(task[0])

            history = m.request_history
            assert history[0].method == 'GET'
            assert history[0].url == 'https://habitica.com/api/v3/tasks/alias'
            assert history[1].method == 'POST'
            assert history[1].url == 'https://habitica.com/api/v3/tasks/user'

    def test_upsert_existing_task_updated_alias(self):
        # Don't test the data, just that the expected API functions are called
        task = get_fake_task(alias='alias')
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/tasks/alias',
                  text=task[1])
            m.put('https://habitica.com/api/v3/tasks/alias',
                  text=task[1])
            self.hs.upsert_task(task[0])

            history = m.request_history
            assert history[0].method == 'GET'
            assert history[0].url == 'https://habitica.com/api/v3/tasks/alias'
            assert history[1].method == 'PUT'
            assert history[1].url == 'https://habitica.com/api/v3/tasks/alias'

    def test_upsert_new_task_created_id(self):
        # Don't test the data, just that the expected API functions are called
        _id = '0934b3fa'
        task = get_fake_task(_id=_id)
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/tasks/'+_id,
                  status_code=requests.codes.not_found)
            m.post('https://habitica.com/api/v3/tasks/user',
                  text=task[1])
            self.hs.upsert_task(task[0])

            history = m.request_history
            assert history[0].method == 'GET'
            assert history[0].url == 'https://habitica.com/api/v3/tasks/'+_id
            assert history[1].method == 'POST'
            assert history[1].url == 'https://habitica.com/api/v3/tasks/user'

    def test_upsert_existing_task_updated_id(self):
        # Don't test the data, just that the expected API functions are called
        _id = '0934b3fa'
        task = get_fake_task(_id=_id)
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/tasks/'+_id,
                  text=task[1])
            m.put('https://habitica.com/api/v3/tasks/'+_id,
                  text=task[1])
            self.hs.upsert_task(task[0])

            history = m.request_history
            assert history[0].method == 'GET'
            assert history[0].url == 'https://habitica.com/api/v3/tasks/'+_id
            assert history[1].method == 'PUT'
            assert history[1].url == 'https://habitica.com/api/v3/tasks/'+_id
