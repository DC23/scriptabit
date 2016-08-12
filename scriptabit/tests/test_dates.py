# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
from datetime import datetime
import pytest
import pytz
import time
from scriptabit.dates import *

def test_parse_date_iso8601_utc():
    raw = '2016-08-12T11:39:08.0Z'
    expected = datetime(2016, 8, 12, 11, 39, 8, tzinfo=pytz.utc)
    actual = parse_date_utc(raw)
    assert actual == expected
    assert actual.tzinfo == pytz.utc

def test_parse_date_epoch_utc_milliseconds():
    raw = '1469601694391'
    expected = datetime(2016, 7, 27, 6, 41, 34, 391000, tzinfo=pytz.utc)
    actual = parse_date_utc(raw, milliseconds=True)
    assert actual == expected
    assert actual.tzinfo == pytz.utc

def test_parse_date_epoch_utc_seconds():
    raw = '1469601694'
    expected = datetime(2016, 7, 27, 6, 41, 34, 0, tzinfo=pytz.utc)
    actual = parse_date_utc(raw, milliseconds=False)
    assert actual == expected
    assert actual.tzinfo == pytz.utc

def test_parse_date_invalid():
    with (pytest.raises(ValueError)):
        parse_date_utc('this is not a date')
