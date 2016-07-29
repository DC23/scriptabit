# -*- coding: utf-8 -*-
""" scriptabit error classes """

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *


# pylint: disable=super-init-not-called
class ConfigError(Exception):
    """Configuration file error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
