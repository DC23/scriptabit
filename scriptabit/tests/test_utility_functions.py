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
                  text=get_fake_stats(hp=10)[1])
            uf = UtilityFunctions(None, self.hs)
            uf.set_health(39)

    def test_set_mana(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(mp=10)[1])
            uf = UtilityFunctions(None, self.hs)
            uf.set_mana(9)

    def test_set_xp(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=get_fake_stats()[1])
            m.put('https://habitica.com/api/v3/user',
                  text=get_fake_stats(exp=10)[1])
            uf = UtilityFunctions(None, self.hs)
            uf.set_xp(39)
