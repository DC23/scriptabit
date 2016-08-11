# -*- coding: utf-8 -*-
""" Error classes """

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


class ServerUnreachableError(Exception):
    """The Habitica server is unreachable"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ArgumentOutOfRangeError(Exception):
    """A function argument is out of range"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PluginError(Exception):
    """Plugin error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidHabiticaDataError(Exception):
    """The specified Habitica data is invalid error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class NotFoundError(Exception):
    """The specified Habitica item was not found error"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
