# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
import pytest
from pkg_resources import resource_filename
# from .common import expect_fail, slow

from scriptabit import habitica_service as hs


# TODO: pytest is not currently detecting the conftest.py file,
# so the slow annotation won't work
# @slow
def test_server_status():
    assert hs.is_server_up() == True
