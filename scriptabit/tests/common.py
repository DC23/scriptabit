# -*- coding: utf-8 -*-
""" common definitions for unit tests """

from pkg_resources import resource_filename

import pytest


# pytest aliases
expect_fail = pytest.mark.xfail

slow = pytest.mark.skipif(
    not pytest.config.getoption('--runslow'),
    reason='Slow test: needs --runslow option to run')
