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

from scriptabit.habitica_service import HabiticaService
from scriptabit.utility_functions import UtilityFunctions

from .fake_data import get_fake_stats

class MockConfig(object):
    def __init__(self, dry_run=False):
        self.dry_run = dry_run

class TestUtilityFunctions(object):

    hs = None

    @classmethod
    def setup_class(cls):
        cls.hs = HabiticaService(
            {},
            'https://habitica.com/api/v3/')

    def test_set_health(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_health(39)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.hp=39'

    def test_inc_health(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=1)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=8)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_health(7, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.hp=8'

    def test_dec_health(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=50)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(hp=29)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_health(-21, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.hp=29'

    def test_set_mana(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=100)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_mana(100)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.mp=100'

    def test_inc_mana(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=30)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=99)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_mana(69, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.mp=99'

    def test_dec_mana(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=50)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_mana(-11, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.mp=39'

    def test_set_xp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=1009)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_xp(1009)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.exp=1009'

    def test_inc_xp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=30)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_xp(9, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.exp=39'

    def test_dec_xp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=500)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=120)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_xp(-380, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.exp=120'

    def test_set_gold(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=9009)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_gold(9009)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.gp=9009'

    def test_inc_gold(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=30)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_gold(9, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.gp=39'

    def test_dec_gold(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=50)[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            uf.set_gold(-11, True)
            history = m.request_history
            assert history[1].method == 'PUT'
            assert history[1].text == 'stats.gp=39'

    def test_set_health_dry_run(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user', text=get_fake_stats()[1])
            uf = UtilityFunctions(MockConfig(dry_run=True), self.hs)
            uf.set_health(39)

            history = m.request_history
            # the put method to set HP should not be called
            assert history[0].method == 'GET'
            assert len(history) == 1

    def test_set_mana_dry_run(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user', text=get_fake_stats()[1])
            uf = UtilityFunctions(MockConfig(dry_run=True), self.hs)
            uf.set_mana(39)

            history = m.request_history
            # the put method to set mana should not be called
            assert history[0].method == 'GET'
            assert len(history) == 1

    def test_set_xp_dry_run(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user', text=get_fake_stats()[1])
            uf = UtilityFunctions(MockConfig(dry_run=True), self.hs)
            uf.set_xp(39)

            history = m.request_history
            # the put method to set XP should not be called
            assert history[0].method == 'GET'
            assert len(history) == 1

    def test_set_gold_dry_run(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user', text=get_fake_stats()[1])
            uf = UtilityFunctions(MockConfig(dry_run=True), self.hs)
            uf.set_gold(39)

            history = m.request_history
            # the put method to set HP should not be called
            assert history[0].method == 'GET'
            assert len(history) == 1
