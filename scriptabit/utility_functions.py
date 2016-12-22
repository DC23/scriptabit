# -*- coding: utf-8 -*-
""" Utility functions
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
from pprint import pprint
from time import sleep

import configargparse
from .dates import parse_date_local
from .habitica_service import HabiticaTaskTypes, SpellIDs

class UtilityFunctions(object):
    """scriptabit utility functions.
    These are a collection of higher-level functions, implemented over the
    `HabiticaService` class.

    Attributes:
        __config (lookupdict): Configuration object returned from argparse.
        __hs (scriptabit.HabiticaService): The HabiticaService instance.
    """
    def __init__(self, config, habitica_service):
        """Initialises the utility functions"""
        self.__config = config
        self.__hs = habitica_service

        self.__stat_setters = [
            {
                'name': 'hp',
                'type': float,
                'default': -1.0,
                'help': 'health points',
                'setter': self.set_health,
            },
            {
                'name': 'mp',
                'type': float,
                'default': -1.0,
                'help': 'mana points',
                'setter': self.set_mana,
            },
            {
                'name': 'xp',
                'type': int,
                'default': -1,
                'help': 'experience points',
                'setter': self.set_xp,
            },
            {
                'name': 'gp',
                'type': float,
                'default': -1.0,
                'help': 'gold',
                'setter': self.set_gold,
            },
        ]

    def get_arg_parser(self):
        """Gets the argument parser containing Utility function CLI arguments.

        Returns:
            argparse.ArgParser:  The ArgParser containing the argument
            definitions.
        """
        parser = configargparse.ArgParser(add_help=False)

        parser.add(
            '-sud',
            '--show-user-data',
            required=False,
            action='store_true',
            help='''Print the user data''')

        for stat in self.__stat_setters:
            # The set arg
            parser.add(
                '-'+stat['name'],
                '--set-'+stat['name'],
                type=stat['type'],
                default=stat['default'],
                required=False,
                help="If > 0, set the user's current {0}".format(stat['help']))

            # The increment/decrement arg
            parser.add(
                # '-'+stat['name'],
                '--inc-'+stat['name'],
                type=stat['type'],
                default=0,
                required=False,
                help="Increment (positive values) or decrement (negative values) the user's current {0}".format(stat['help']))

        parser.add(
            '--delete-todos',
            required=False,
            action='store_true',
            help='''Delete all current To-do tasks''')

        parser.add(
            '--buy-armoire',
            required=False,
            action='store_true',
            help='''Purchase an item from the armoire''')

        parser.add(
            '--list-tasks',
            required=False,
            action='store_true',
            help='''List all tasks, in raw dictionary format.''')

        parser.add(
            '-t',
            '--test',
            required=False,
            action='store_true',
            help='''Run the current test function''')

        return parser

    @property
    def dry_run(self):
        """ Indicates whether this is a dry run or not.

        Returns:
            bool: True if this is a dry run, otherwise False.
        """
        return self.__config.dry_run

    def run(self):
        """Runs the user-selected scriptabit utility functions"""
        if self.__config.test:
            self.__test()
            return

        if self.__config.show_user_data:
            self.show_user_data()

        if self.__config.delete_todos:
            self.delete_todos()

        if self.__config.buy_armoire:
            self.buy_armoire()

        if self.__config.list_tasks:
            self.list_tasks()

        config_dict = vars(self.__config)

        # dispatch any setters and incrementers
        for stat in self.__stat_setters:
            arg = config_dict['set_'+stat['name']]
            if arg >= 0:
                stat['setter'](arg)

            inc_arg = config_dict['inc_'+stat['name']]
            if inc_arg != 0:
                stat['setter'](inc_arg, increment=True)

    def __set_stat(
            self,
            name,
            value,
            hs_func,
            lower_bound=0,
            increment=False):
        """Generic stat setter.

        Args:
            name (str): The stat name
            value: the new value
            hs_func: The HabiticaService method that will set the stat.
            lower_bound: Lower bound on the set value
            increment (bool): If true, the value is treated as an increment
                instead of the new value

        Returns:
            The new stat value
        """
        old = self.__hs.get_stats()[name]
        set_value = old + value if increment else value
        set_value = max(lower_bound, set_value)
        new = set_value if self.dry_run else hs_func(set_value)
        logging.getLogger(__name__).info(
            '%s changed from %f to %f',
            name,
            old,
            new)
        return new

    def set_health(self, hp, increment=False):
        """Sets the user health to the specified value

        Returns:
            float: The new health points.
        """
        return self.__set_stat('hp', hp, self.__hs.set_hp, increment=increment)

    def set_xp(self, xp, increment=False):
        """Sets the user experience points to the specified value.

        Returns:
            int: The new experience points.
        """
        return self.__set_stat('exp', xp, self.__hs.set_exp, increment=increment)

    def set_mana(self, mp, increment=False):
        """Sets the user mana to the specified value

        Returns:
            float: The new mana points.
        """
        return self.__set_stat('mp', mp, self.__hs.set_mp, increment=increment)

    def set_gold(self, gp, increment=False):
        """Sets the user gold to the specified value

        Returns:
            float: The new gold points.
        """
        return self.__set_stat('gp', gp, self.__hs.set_gp, increment=increment)

    def show_user_data(self):
        """Shows the user data"""
        logging.getLogger(__name__).debug('Getting user data')
        data = self.__hs.get_user()
        print()
        print("Summarised User Data")
        print("--------------------")
        print()
        print(data['profile']['name'])
        print("Last Cron: {0}".format(parse_date_local(data['lastCron'])))
        pprint(data['stats'])
        print()
        print("--------------------")
        print()

    @staticmethod
    def upsert_notification(
            habitica_service,
            text,
            notes='',
            heading_level=0,
            append_time=True,
            tags=None,
            alias='scriptabit_notification_panel'):
        """ Creates or updates a notification (currently implemented as a
        scoreless habit).

        Args:
            habitica_service (HabiticaService): The habitica service to use.
            text (str): the new text.
            notes (str): the extra text/notes.
            heading_level (int): If > 0, Markdown heading syntax is
                prepended to the message text.
            append_time (bool): If True, a time stamp is appended to text.
            tags (list): Optional list of tags to be applied to
                the notification.
            alias (str): the notification alias.

        Returns:
            dict: The notification object returned by the Habitica API
        """
        heading_level = min(heading_level, 6)
        if heading_level > 0:
            text = '#' * heading_level + ' ' + text

        if append_time:
            text = '{0} @ {1}'.format(text, datetime.now().strftime('%X %x'))

        task = {
            'alias': alias,
            'up': 'false',
            'down': 'false',
            'text': text,
            'notes': notes,
            }

        tags = tags or ['scriptabit']
        tags = habitica_service.create_tags(tags)
        task['tags'] = [t['id'] for t in tags]

        return habitica_service.upsert_task(
            task,
            task_type=HabiticaTaskTypes.habits)

    def delete_todos(self):
        """Deletes all user todos"""
        logging.getLogger(__name__).debug('Deleting all todos')
        tasks = self.__hs.get_tasks(task_type=HabiticaTaskTypes.todos)
        for t in tasks:
            print('Deleting {0}'.format(t['text']))
            if not self.dry_run:
                self.__hs.delete_task(t)

    def buy_armoire(self):
        """Purchase an item from the Enchanted Armoire"""
        logging.getLogger(__name__).debug("Checking the armoire...")
        for _ in range(self.__config.max_updates or 1):
            if not self.__config.dry_run:
                data = self.__hs.buy_armoire()
            else:
                data = {'message': "Dry run"}
            print(data['message'])
            sleep(2)

    def list_tasks(self):
        """Dumps all tasks"""
        print('all tasks')
        tasks = self.__hs.get_tasks()
        for t in tasks:
            pprint(t)

    def __test(self):
        """A test function. Could do anything depending on what I am testing."""
        print()
        logging.getLogger(__name__).debug('Running test function')
        print("--------------------")
        print("--------------------")
        print()
