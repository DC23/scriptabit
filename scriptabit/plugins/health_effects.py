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
import glob
import logging
import math
import os
import pickle
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
            help='Health Effects: Sun HP damage multiplier for vampire mode.')

        parser.add(
            '--moon-power',
            required=False,
            default=1.0,
            type=float,
            help='Health Effects: Moonlight HP restoration multiplier for vampire mode.')

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
            msg = ':full_moon: Ahh, sweet moonlight. {hp:.2} HP per hour'
        else:
            hp24 = hp24_day
            msg = ':sunny: The Sun! It burns! {hp:.2} HP per hour'

        # apply the health change
        delta = self.apply_health_delta(hp24=hp24, up=night)

        delta_per_hour = hp24 / 24
        if not night:
            delta_per_hour *= -1

        print('applied delta', delta)
        print('delta_per_hour', delta_per_hour)

        # Notifications
        self.notify(
            msg.format(hp=delta_per_hour),
            tags=['scriptabit', 'vampire'],
            alias='vampire_notification_panel')

        return True

    def summarise_task_score(self, task, now, window):
        """ Summarises the task score changes within a time window.

        Args:
            task (dict): The task.
            now (datetime): The most recent time to consider.
            window (timedelta): The time window to consider prior to now.

        Returns:
            float: Total of the score changes within the time window.
            int: Number of times the score went up.
            int: Number of times the score went down.
        """
        if task['type'] == 'todo':
            if task['completed']:
                return float(task['value']) * float(task['priority']), 1, 0
            else:
                return 0, 0, 0

        if 'history' not in task:
            return 0, 0, 0

        def pairwise(iterable):
            """ pairwise iteration of a sequence.

            s -> (s0,s1), (s1,s2), (s2, s3), ...

            """
            a, b = itertools.tee(iterable)
            next(b, None)
            return zip(a, b)

        class PairCounter(object):
            """ Tracks score movements for a pair of values. """
            def __init__(self, scale=1):
                """ Initialises the PairCounter.

                Args:
                    multiplier (float): Optional score scale factor.
                """
                self.up = 0
                self.down = 0
                self.sum_delta = 0
                self.scale = scale

            def count(self, a, b):
                """ Count a pair of values. """
                delta = (b - a) * self.scale
                # print(a, b, delta)
                self.sum_delta += delta
                if delta > 0:
                    self.up += 1
                elif delta < 0:
                    self.down += 1

        counter = PairCounter()
        # counter = PairCounter(3 if task['type'] == 'daily' else 1)
        history = [{'date': task['createdAt'], 'value': 0}]
        history.extend(task['history'])

        # print()
        # print(task['text'])
        # pprint(history)

        for a, b in pairwise(history):
            date = scriptabit.parse_date_utc(b['date'])
            if date <= now and now - date < window:
                counter.count(a['value'], b['value'])

        return counter.sum_delta, counter.up, counter.down

    def test(self):
        """ Health effects test function.

        Could do anything depending on what I need to test.
        """
        def live():
            all_tasks = self._hs.get_tasks()
            # all_tasks.extend(
                # self._hs.get_tasks(
                    # task_type=scriptabit.HabiticaTaskTypes.completed_todos))
            self.summarise_task_performance(all_tasks)

        def save():
            filename = './dc_sep_06.p'
            all_tasks = self._hs.get_tasks()
            with open(filename, 'wb') as f:
                pickle.dump(all_tasks, f, pickle.HIGHEST_PROTOCOL)

            self.summarise_task_performance(all_tasks)

        def load(filename):
            print()
            print('------------------------------')
            print(filename)
            with open(filename, 'rb') as f:
                all_tasks = pickle.load(f)

            dailies = self.summarise_task_performance(
                [t for t in all_tasks if t['type'] == 'daily'])

            habits = self.summarise_task_performance(
                [t for t in all_tasks if t['type'] == 'habit'])

            pprint(dailies)
            pprint(habits)

        def load_all():
            results = {}
            for filename in glob.glob("*.p"):
                results[filename] = load(filename)
            pprint(results)

        live()
        # save()
        # load_all()
        # load('dc_sep_06.p')
        return False

    def logistic_growth(
            self,
            x,
            a=50,
            b=0.5,
            k_x_positive=0.2,
            k_x_negative=4.8):
        """ Returns the logistic growth function value for a given input x.

        y = a / (1 + b * e^(kx))

        For k > 0, larger values give a greater rate of change while smaller
        values lead to a slower approach to the function asymptotes.

        For positive k, the return values is bounded by a to the left
        (large negative x) and by 0 to the right (large positive x). For
        negative k this is reversed.

        Additionally, this method allows different k terms for positive and
        negative x, which allows finer-grained tuning of the output.

        The y-intercept is given by a / (1 + b).

        Args:
            x (float): The input value
            a (float): The upper limit on the function value.
            b (float): Influences the steepness of the function curve, and also
                contributes to the y-intercept. High values give a slower change
                and a lower y-intercept.
            k_x_positive (float): The k term used when x >= 0
            k_x_negative (float): The k term used when x < 0. Passing None will
                cause k_x_positive to be used for all x.

        Returns:
            float: The delta.
        """
        assert b >= 0
        k = k_x_positive if x >= 0 or not k_x_negative else k_x_negative
        y = a / (1 + b * math.exp(k * x))
        return y

    def summarise_task_performance(self, tasks, window_hours=24):
        """ Summarises overall task performance within a time window back from
        the current time.

        Args:
            tasks (list): The list of Habitica tasks to summarise.
            window_hours (float): Size of the time window in hours

        Returns:
        """
        now = datetime.now(tz=pytz.utc)
        window = timedelta(hours=window_hours)

        up = 0
        down = 0
        total_delta = 0
        for t in tasks:
            tot_delta, tup, tdown = self.summarise_task_score(t, now, window)

            # only track those tasks in which something changed inside the time
            # window. If nothing changed, there will be no up or down counts.
            if tup + tdown:
                up += tup
                down += tdown
                total_delta += tot_delta

        count = up + down
        avg_delta = total_delta / count if count else 0

        print()
        # pprint(tasks)
        print('window', window)
        print('up', up)
        print('down', down)
        print('Total up + down', count)
        print('total_delta', total_delta)
        print('avg_delta', avg_delta)
        print('logistic fn(total delta)', self.logistic_growth(total_delta))
        print('logistic fn(avg delta)', self.logistic_growth(avg_delta))

        return down, up, total_delta, avg_delta

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
        elif self._config.test:
            try:
                return self.test()
            except Exception as e:
                logging.getLogger(__name__).error(e)
                import traceback
                traceback.print_exc()

        # If no other functions ran, just print the help and exit
        self.__print_help()
        return False
