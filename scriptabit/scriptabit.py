# -*- coding: utf-8 -*-

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *


def poisoner():
    """ Command-line entry point for scriptabit """
    print('scriptabit placeholder CLI entry point')


def start_gui():
    """ GUI entry point for scriptabit """
    print('scriptabit placeholder GUI entry point')


if __name__ == 'main':
    poisoner()
