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
from pprint import pprint

import configargparse
from .dates import parse_date_local
from .habitica_service import HabiticaTaskTypes

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

    @classmethod
    def get_arg_parser(cls):
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

        parser.add(
            '-hp',
            '--set-hp',
            type=float,
            default=-1.0,
            required=False,
            help='''If > 0, set the user's current HP''')

        parser.add(
            '-mp',
            '--set-mp',
            type=float,
            default=-1.0,
            required=False,
            help='''If > 0, set the user's current MP (mana points)''')

        parser.add(
            '-xp',
            '--set-xp',
            type=int,
            default=-1,
            required=False,
            help='''If > 0, set the user's current XP (experience points)''')

        parser.add(
            '-gp',
            '--set-gp',
            type=float,
            default=-1.0,
            required=False,
            help='''If > 0, set the user's current gold (gold points)''')

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

        if self.__config.set_hp >= 0:
            self.set_health(self.__config.set_hp)

        if self.__config.set_mp >= 0:
            self.set_mana(self.__config.set_mp)

        if self.__config.set_xp >= 0:
            self.set_xp(self.__config.set_xp)

        if self.__config.set_gp >= 0:
            self.set_gold(self.__config.set_gp)

        if self.__config.delete_todos:
            self.delete_todos()

        if self.__config.buy_armoire:
            self.buy_armoire()

    def set_health(self, hp):
        """Sets the user health to the specified value

        Returns:
            float: The new health points.
        """
        old_hp = self.__hs.get_stats()['hp']
        new_hp = hp if self.dry_run else self.__hs.set_hp(hp)
        logging.getLogger(__name__).info(
            'HP changed from %f to %f',
            old_hp,
            new_hp)
        return new_hp

    def set_xp(self, xp):
        """Sets the user experience points to the specified value.

        Returns:
            int: The new experience points.
        """
        old_xp = self.__hs.get_stats()['exp']
        new_xp = xp if self.dry_run else self.__hs.set_exp(xp)
        logging.getLogger(__name__).info(
            'XP changed from %f to %f',
            old_xp,
            new_xp)
        return new_xp

    def set_mana(self, mp):
        """Sets the user mana to the specified value

        Returns:
            float: The new mana points.
        """
        old_mp = self.__hs.get_stats()['mp']
        new_mp = mp if self.dry_run else self.__hs.set_mp(mp)
        logging.getLogger(__name__).info(
            'MP changed from %f to %f',
            old_mp,
            new_mp)
        return new_mp

    def set_gold(self, gp):
        """Sets the user gold to the specified value

        Returns:
            float: The new gold points.
        """
        old = self.__hs.get_stats()['gp']
        new = gp if self.dry_run else self.__hs.set_gp(gp)
        logging.getLogger(__name__).info(
            'Gold changed from %f to %f',
            old,
            new)
        return new

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
            tags (list): Optional list of tags to be applied to
                the notification.
            alias (str): the notification alias.

        Returns:
            dict: The notification object returned by the Habitica API
        """
        heading_level = min(heading_level, 6)
        if heading_level > 0:
            text = '#' * heading_level + ' ' + text

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
            data = self.__hs.buy_armoire()
            print(data['message'])

    def __test(self):
        """A test function. Could do anything depending on what I am testing."""
        print()
        logging.getLogger(__name__).debug('Running test function')
        print("--------------------")
        data = self.__hs.buy_armoire()
        pprint(data['message'])
        print("--------------------")
        print()
