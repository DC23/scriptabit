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
import configargparse

from yapsy.IPlugin import IPlugin as YapsyIPlugin

from .utility_functions import UtilityFunctions


# pylint: disable=no-self-use
class IPlugin(YapsyIPlugin):
    """ Scriptabit plugin base class.

    Attributes:
        _config (lookupdict): Configuration object returned from argparse.
        _update_count (int): Number of updates (zero-based).
        _hs (scriptabit.HabiticaService): The HabiticaService instance.
    """

    def __init__(self):
        """ Initialises the plugin. It is hard to do any significant work here
        as the yapsy framework instantiates plugins automatically. Thus extra
        arguments cannot be passed easily.
        """
        super().__init__()
        self._config = None
        self._update_count = 0
        self._hs = None
        self._data_dir = None

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

    @staticmethod
    def supports_dry_runs():
        """ Indicates whether the plugin correctly supports the `dry-run`
        command-line flag.

        To support dry runs, the plugin must not modify any persistent data,
        either on Habitica or elsewhere if the `dry-run` flag is True.

        Returns:
            bool: True if dry runs are supported, otherwise False.
        """
        return False

    @property
    def dry_run(self):
        """ Indicates whether this is a dry run or not.

        Returns:
            bool: True if this is a dry run, otherwise False.
        """
        return self._config.dry_run

    def notify(
            self,
            message,
            **kwargs):
        """ Notify the Habitica user.

        If this is a dry run, then the message is logged. Otherwise the message
        is logged and posted to the Habitica notification panel.

        Args:
            message (str): The message.
            panel (bool): If True, the Habitica panel is updated.
            notes (str): the extra text/notes.
            heading_level (int): If > 0, Markdown heading syntax is
                prepended to the message text.
            tags (list): Optional list of tags to be applied to
                the notification.
            alias (str): the notification alias.
        """
        logging.getLogger(__name__).info(message)

        panel = kwargs.pop('panel', True)

        if panel and not self.dry_run:
            UtilityFunctions.upsert_notification(
                self._hs,
                text=message,
                **kwargs)

    def activate(self):
        """ Called by the plugin framework when a plugin is activated."""
        pass

    def deactivate(self):
        """ Called by the plugin framework when a plugin is deactivated."""
        pass

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the plugin.

        Generally, any initialisation should be done here rather than in
        activate or __init__.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        self._config = configuration
        self._hs = habitica_service
        self._data_dir = data_dir

    def update_interval_seconds(self):
        """ Indicates the required update interval in integer seconds.

        Returns:
            int: update interval in whole seconds
        """
        return int(self.update_interval_minutes() * 60)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns:
            float: The required update interval in minutes.
        """
        return max(5, self._config.update_frequency)

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns:
            bool: True if further updates are required; False if the plugin
            is finished and the application should shut down.
        """
        self._update_count += 1
        return False
