"""Scriptabit plugin that implements a poisoning/health
regeneration scenario based on player performance on dailies.

**Not implemented yet**
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

import scriptabit


class HealthEffects(scriptabit.IPlugin):
    """ Implements the health effects plugin.
    """
    def __init__(self):
        """ Initialises the plugin.
        """
        super().__init__()
        self.__print_help = None

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.
        """
        parser = super().get_arg_parser()

        parser.add(
            '-hp24',
            '--max-hp-change-per-day',
            required=False,
            default=10.0,
            type=float,
            help='Health Effects: Max amount of health change per day')

        parser.add(
            '--health-drain',
            required=False,
            action='store_true',
            help='Drains your health over time')

        self.__print_help = parser.print_help

        return parser

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        super().initialise(configuration, habitica_service, data_dir)
        logging.getLogger(__name__).info('HealthEffects initialising')

    @staticmethod
    def supports_dry_runs():
        """ The HealthEffects plugin supports dry runs.

        Returns:
            bool: True
        """
        return True

    def get_health_delta(self):
        """ Gets the health delta for the current update """
        hp24 = self._config.max_hp_change_per_day
        interval = self.update_interval_minutes()
        return interval * hp24 / (24 * 60)

    def poisoned(self):
        """ Simple health drain/poisoning """
        hp_delta = self.get_health_delta()
        logging.getLogger(__name__).info('Poisoning %f HP', hp_delta)
        return False

    def update(self):
        """ Update the health effects plugin.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        super().update()
        if self._config.health_drain:
            return self.poisoned()

        # If no other functions ran, just print the help and exit
        self.__print_help()
        return False
