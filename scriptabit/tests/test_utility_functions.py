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
            assert uf.set_health(39) == 39

    def test_set_mana(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=9)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            assert uf.set_mana(9) == 9

    def test_set_xp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=39)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            assert uf.set_xp(39) == 39

    def test_set_gold(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(gp=9009)[1])
            uf = UtilityFunctions(MockConfig(), self.hs)
            assert uf.set_gold(9009) == 9009

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
