"""Scriptabit plugin that implements various health-modification effects.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import itertools
import logging
from datetime import datetime, timedelta
from pprint import pprint

import pytz
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

        parser.add(
            '--htest',
            required=False,
            action='store_true',
            help='health effects test function')

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

    def summarise_task_score(self, task, now, window):
        def pairwise(iterable):
            "s -> (s0,s1), (s1,s2), (s2, s3), ..."
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)

        up = 0
        down = 0
        history = task['history']
        sum_delta = 0
        if len(history) == 1:
            a = history[0]
            date = scriptabit.parse_date_utc(a['date'])
            if now - date < window:
                delta = a['value']
                sum_delta += delta
                if delta > 0:
                    up += 1
                elif delta < 0:
                    down += 1
        else:
            for a, b in pairwise(history):
                b_date = scriptabit.parse_date_utc(b['date'])
                if now - b_date < window:
                    delta = b['value'] - a['value']
                    sum_delta += delta
                    if delta > 0:
                        up += 1
                    elif delta < 0:
                        down += 1

        return sum_delta, up, down

    def test(self):
        """ Health effects test function.

        Could do anything depending on what I need to test.
        """
        # Lets try getting all habits and dailies, and some stats on recent
        # score changes
        now = datetime.now(tz=pytz.utc)
        window = timedelta(days=1)
        all_tasks = self._hs.get_tasks()
        tasks = [t for t in all_tasks if t['type'] in ['habit', 'daily']]
        changed = []
        up = 0
        down = 0
        total_delta = 0
        count = 0
        for t in tasks:
            tot_delta, tup, tdown = self.summarise_task_score(
                t, now, window)

            if tup + tdown:
                count += 1
                up += tup
                down += tdown
                total_delta += tot_delta
                stat = {
                    'id': t['_id'],
                    'text': t['text'],
                    'last_change': t['updatedAt'],
                    'tot_delta': tot_delta,
                    'tup': tup,
                    'tdown': tdown,
                }
                changed.append(stat)

        # pprint(changed)
        # pprint(tasks)
        print('up', up)
        print('down', down)
        print('total_delta', total_delta)
        print('avg_delta', total_delta / count if count else 0)

        todo_score = 0
        todo_count = 0
        for t in all_tasks:
            if t['type'] == 'todo':
                todo_score += t['value']
                todo_count += 1

        print('todo score', todo_score)
        print('todo count', todo_count)
        print('todo avg', todo_score / todo_count if todo_count else 'NaN')

        return False

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
        elif self._config.htest:
            return self.test()

        # If no other functions ran, just print the help and exit
        self.__print_help()
        return False
