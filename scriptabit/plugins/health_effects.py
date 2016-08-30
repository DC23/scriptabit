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
        self.__stats = None

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

        parser.add(
            '--health-regen',
            required=False,
            action='store_true',
            help='Restores your health over time')

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
        hp24 = abs(self._config.max_hp_change_per_day)
        interval = self.update_interval_minutes()
        return interval * hp24 / (24 * 60)

    def apply_health_delta(self, up=True):
        """ Applies the health delta.

        Args:
            up (bool): If True, then health is increased, otherwise health is
                decreased.

        Returns:
            float: the signed health delta that was applied.
        """
        delta = self.get_health_delta()
        old_hp = self.__stats['hp']

        if up:
            new_hp = max(50, old_hp + delta)
        else:
            new_hp = max(0, old_hp - delta)

        if not self.dry_run:
            self._hs.set_hp(new_hp)

        return delta if up else -delta

    def poisoned(self):
        """ Simple health drain/poisoning """
        delta = abs(self.apply_health_delta(up=False))
        self.notify('Poisoned. Lost {0:.2} HP'.format(delta), panel=False)
        return True

    def regenerating(self):
        """ Simple health regeneration """
        delta = self.apply_health_delta(up=True)
        self.notify('Regenerated {0:.2} HP'.format(delta), panel=False)
        return True

    def update(self):
        """ Update the health effects plugin.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        super().update()

        # get some user data
        self.__stats = self._hs.get_stats()

        if self._config.health_drain:
            return self.poisoned()
        elif self._config.health_regen:
            return self.regenerating()

        # If no other functions ran, just print the help and exit
        self.__print_help()
        return False
