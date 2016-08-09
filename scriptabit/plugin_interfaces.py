# -*- coding: utf-8 -*-
""" The scriptabit plugin interfaces.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

from yapsy.IPlugin import IPlugin


class IOfficialPlugin(IPlugin):
    """Internal class intended to allow identification of the builtin
    plugins.
    """

    def activate(self):
        """ Called by the plugin framework when a plugin is activated."""

        logging.getLogger(__name__).debug('%s activated', self.id())

    def deactivate(self):
        """ Called by the plugin framework when a plugin is deactivated."""
        logging.getLogger(__name__).debug('%s deactivated', self.id())


class IUserPlugin(IOfficialPlugin):
    """Base class/interface for user plugins.

    Does not add any extra functionality to the superclass `IOfficialPlugin`,
    but it allows filtering the plugins into official/user categories.
    """

    pass
