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
from pkg_resources import resource_filename

from scriptabit.habitica_service import HabiticaService


class TestHabiticaService(object):

    hs = None

    def setup_class(cls):
        cls.hs = HabiticaService(
            requests,
            {},
            'https://habitica.com/api/v3/')

    def test_server_status(self):
        assert self.hs.is_server_up() == True
