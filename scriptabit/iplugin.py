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
import configargparse

from yapsy.IPlugin import IPlugin as YapsyIPlugin


# pylint: disable=no-self-use
class IPlugin(YapsyIPlugin):
    """ Scriptabit plugin base class.

    Attributes:
        config (lookupdict): Configuration object returned from argparse.
        update_count (int): Number of updates (zero-based).
        hs (scriptabit.HabiticaService): The HabiticaService instance.
    """

    def __init__(self):
        """ Initialises the plugin. It is hard to do any significant work here
        as the yapsy framework instantiates plugins automatically. Thus extra
        arguments cannot be passed easily.
        """

        super().__init__()
        self.config = None
        self.update_count = 0
        self.hs = None

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Note that to avoid argument name conflicts, only long argument names
        should be used, and they should be prefixed with the plugin-name or
        unique abbreviation.

        To get their `ArgParser`, subclasses should call this method via super
        and capture the returned `ArgParser` instance.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """

        return configargparse.ArgParser(add_help=False)

    def activate(self):
        """ Called by the plugin framework when a plugin is activated."""

        pass

    def deactivate(self):
        """ Called by the plugin framework when a plugin is deactivated."""

        pass

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """

        self.config = configuration
        self.hs = habitica_service

    def update_interval_seconds(self):
        """ Indicates the required update interval in integer seconds.

        Returns: int: update interval in whole seconds
        """

        return int(self.update_interval_minutes() * 60)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        This method will be ignored when single_shot returns True.
        The default interval is 60 minutes.

        Returns: float: The required update interval in minutes.
        """

        return 60

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """

        self.update_count += 1
        return False
