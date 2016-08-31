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
from datetime import datetime

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
            '--sun-power',
            required=False,
            default=2.0,
            type=float,
            help='Health Effects: Sun HP damage multiplier.')

        parser.add(
            '--moon-power',
            required=False,
            default=1.0,
            type=float,
            help='Health Effects: Moonlight HP restoration multiplier.')

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

        parser.add(
            '--vampire',
            required=False,
            action='store_true',
            help='Enables Vampire mode')

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

    @staticmethod
    def supports_dry_runs():
        """ The HealthEffects plugin supports dry runs.

        Returns:
            bool: True
        """
        return True

    def get_health_delta(self, hp24=None):
        """ Gets the health delta for the current update """
        hp24 = abs(hp24 or self._config.max_hp_change_per_day)
        interval = self.update_interval_minutes()
        return interval * hp24 / (24 * 60)

    def apply_health_delta(self, hp24=None, up=True):
        """ Applies the health delta.

        Args:
            hp24 (float): The health change per 24 hours.
            up (bool): If True, then health is increased, otherwise health is
                decreased.

        Returns:
            float: the signed health delta that was applied.
        """
        delta = self.get_health_delta(hp24)
        old_hp = self.__stats['hp']

        if up:
            new_hp = min(50, old_hp + delta)
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

    def vampire(self):
        """ Vampire mode.

        Lose health during daylight hours.
        Gain small amounts of health at night, and large amounts by feeding.
        """
        logging.getLogger(__name__).debug('You are a Vampire!')

        moon_power = self._config.moon_power
        sun_power = self._config.sun_power
        hp24 = self._config.max_hp_change_per_day
        hp24_night = hp24 * moon_power
        hp24_day = hp24 * sun_power
        print('Moon power multiplier: {0:.4}'.format(moon_power))
        print('Sun power multiplier: {0:.4}'.format(sun_power))
        print('HP Change per 24 hours: {0:.4}'.format(hp24))
        print('Max HP loss during the day: {0:.4}'.format(hp24_day / 2))
        print('Max HP gain during the night: {0:.4}'.format(hp24_night / 2))

        # determine day or night mode
        # Night is 6pm (1800) to 6am (0600)
        now = datetime.now()
        night = now.hour < 6 or now.hour >= 18

        # Are we regenerating or taking damage?
        if night:
            hp24 = hp24_night
            msg = ':full_moon: Ahh, sweet moonlight. {hp:.2} HP'
        else:
            hp24 = hp24_day
            msg = ':sunny: The Sun! It burns! {hp:.2} HP'

        # apply the health change
        delta = self.apply_health_delta(hp24=hp24, up=night)

        # Notifications
        self.notify(
            msg.format(hp=delta),
            tags=['scriptabit', 'vampire'],
            alias='vampire_notification_panel')

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
        elif self._config.vampire:
            return self.vampire()

        # If no other functions ran, just print the help and exit
        self.__print_help()
        return False
