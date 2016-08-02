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

from scriptabit.habitica_service import HabiticaService


class TestHabiticaService(object):

    hs = None

    def _get_stats_json(self,
                        con=10,
                        _int=11,
                        per=12,
                        _str=13,
                        gp=194.4,
                        hp=47.21,
                        lvl=4,
                        exp=34,
                        toNextLevel=180):
        return '''{"data": {
        "stats": {"buffs": {"con": 2,
        "int": 2,
        "per": 2,
        "seafoam": False,
        "shinySeed": False,
        "snowball": False,
        "spookySparkles": False,
        "stealth": 0,
        "str": 2,
        "streaks": False},
        "class": "warrior",
        "con": {0},
        "exp": {7},
        "gp": {4},
        "hp": {5},
        "int": {1},
        "lvl": {6},
        "maxHealth": 50,
        "maxMP": 38,
        "mp": 38,
        "per": {2},
        "points": 4,
        "str": {3},
        "toNextLevel": {8},
        "training": {"con": 0, "int": 0, "per": 0, "str": 0}},
        }}'''.format(
            con,
            _int,
            per,
            _str,
            gp,
            hp,
            lvl,
            exp,
            toNextLevel)

    def setup_class(cls):
        cls.hs = HabiticaService(
            {},
            'https://habitica.com/api/v3/')

    def test_server_status_up(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/status',
                  text='''{"data": {"status": "up"}}''')
            assert self.hs.is_server_up() == True

    def test_server_status_down(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/status',
                  text='''{"data": {"status": "down"}}''')
            assert self.hs.is_server_up() == False

    def test_get_user_stats(self):
        with requests_mock.mock() as m:
            m.get('https://habitica.com/api/v3/user',
                  text=self._get_stats_json(
                        con=10,
                        _int=11,
                        per=12,
                        _str=13,
                        gp=194.4,
                        hp=47.21,
                        lvl=4,
                        exp=34,
                        toNextLevel=180))
            stats = self.hs.get_user_stats()

            assert stats['con'] == 10
            assert stats['int'] == 11
            assert stats['per'] == 12
            assert stats['str'] == 13
            assert stats['hp'] == 47.21
            assert stats['lvl'] == 4
            assert stats['exp'] == 34
            assert stats['toNextLevel'] == 180
