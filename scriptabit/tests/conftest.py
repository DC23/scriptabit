# -*- coding: utf-8 -*-
""" PyTest configuration """

import pytest

def pytest_addoption(parser):
    # creates a command line option to run slow tests
    parser.addoption("--runslow", action="store_true", help="run slow tests")
