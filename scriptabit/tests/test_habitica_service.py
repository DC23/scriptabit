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

    def setup_class(cls):
        cls.hs = HabiticaService(
            {},
            'https://habitica.com/api/v3/')

    def test_server_status_up(self):
        with requests_mock.mock() as m:
            m.get(
            'https://habitica.com/api/v3/status',
            text='''{"data": {"status": "up"}}''')
            assert self.hs.is_server_up() == True

    def test_server_status_down(self):
        with requests_mock.mock() as m:
            m.get(
            'https://habitica.com/api/v3/status',
            text='''{"data": {"status": "down"}}''')
            assert self.hs.is_server_up() == False
