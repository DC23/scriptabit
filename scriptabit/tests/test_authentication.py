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

import scriptabit as sb
from ..authentication import load_habitica_authentication_credentials
from ..errors import ConfigError


def test_load_valid():
    cfg = resource_filename(sb.__name__, 'tests/data/auth.cfg')
    credentials = load_habitica_authentication_credentials(cfg, section='Habitica')
    assert credentials['x-api-key'] == 'default_key'
    assert credentials['x-api-user'] == 'default_user'

def test_load_missing_section():
    cfg = resource_filename(sb.__name__, 'tests/data/auth.cfg')
    with pytest.raises(ConfigError):
        load_habitica_authentication_credentials(cfg, section='Missing')

def test_load_missing_user():
    cfg = resource_filename(sb.__name__, 'tests/data/auth.cfg')
    with pytest.raises(ConfigError):
        load_habitica_authentication_credentials(cfg, section='missing_user')

def test_load_missing_key():
    cfg = resource_filename(sb.__name__, 'tests/data/auth.cfg')
    with pytest.raises(ConfigError):
        load_habitica_authentication_credentials(cfg, section='missing_key')

def test_load_missing_file():
    with pytest.raises(ConfigError):
        load_habitica_authentication_credentials('missingfile.cfg')
