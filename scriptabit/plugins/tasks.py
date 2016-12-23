# -*- coding: utf-8 -*-
"""Task manipulation plugin
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
from time import sleep
from pprint import pprint
import logging

# from .dates import parse_date_local
# from .habitica_service import HabiticaTaskTypes, SpellIDs
import scriptabit as sb

class Tasks(sb.IPlugin):
    """ Tasks plugin implementation
    """
    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()
        self._print_help = None

    @staticmethod
    def supports_dry_runs():
        """ Do we support dry runs?

        Returns:
            bool: True
        """
        return True

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Note that to avoid argument name conflicts, only long argument names
        should be used, and they should be prefixed with the plugin-name or
        unique abbreviation.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--delete-tasks',
            required=False,
            action='store_true',
            help='''Delete all tasks''')

        parser.add(
            '--list-tasks',
            required=False,
            action='store_true',
            help='''List all tasks.''')

        parser.add(
            '--task-type',
            required=False,
            default='all',
            type=str,
            choices=['habits', 'dailys', 'todos', 'rewards', 'all'],
            help='Specify the task type to operate on')

        self._print_help = parser.print_help
        return parser

    def print_help(self):
        """ Print the help text """
        if self._print_help:
            self._print_help()

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
        super().initialise(configuration, habitica_service, data_dir)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        # minimum update frequency of once every 1 minute, or whatever the
        # user specified
        return max(5, self._config.update_frequency)

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """

        print(self._config.task_type)
        if self._config.list_tasks:
            self.list_tasks()
        elif self._config.delete_tasks:
            self.delete_tasks()
        else:
            print()
            self.print_help()

        # return False if finished, and True to be updated again.
        return False

    def delete_tasks(self):
        """Deletes all user tasks"""
        logging.getLogger(__name__).debug('Deleting all tasks')
        tasks = self._hs.get_tasks(task_type=sb.HabiticaTaskTypes.todos)
        for t in tasks:
            print('Deleting {0}'.format(t['text']))
            if not self.dry_run:
                self._hs.delete_task(t)

    def list_tasks(self):
        """Dumps all tasks"""
        print('*** Listing All Tasks ***')
        print()
        tasks = self._hs.get_tasks()
        for t in tasks:
            if self._config.verbose:
                pprint(t)
            else:
                print(t['text'])
