# -*- coding: utf-8 -*-
""" Unit tests for the banking plugin """
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from .banking import Banking

def test_get_balance_from_string():
    """test_get_balance_from_string"""
    expected = 508
    s = 'Balance: {0}'.format(expected)
    actual = Banking.get_balance_from_string(s)
    assert expected == actual

def test_get_balance_string():
    """test_get_balance_string"""
    expected = 'Balance: 97'
    actual = Banking.get_balance_string(97)
    assert expected == actual

def test_get_zero_balance_from_empty_string():
    """an empty string should equate to a zero balance"""
    assert Banking.get_balance_from_string('') == 0

def test_get_zero_balance_from_string_without_numbers():
    """a string without numbers should equate to a zero balance"""
    assert Banking.get_balance_from_string('blah blah blah') == 0
