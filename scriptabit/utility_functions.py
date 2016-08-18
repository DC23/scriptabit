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
from .habitica_task import HabiticaTask

class UtilityFunctions(object):
    """scriptabit utility functions.
    These are a collection of higher-level functions, implemented over the
    `HabiticaService` class.

    Attributes:
        __config (lookupdict): Configuration object returned from argparse.
        __hs (scriptabit.HabiticaService): The HabiticaService instance.
    """

    __config = None
    __hs = None

    def __init__(self, config, habitica_service):
        """Initialises the utility functions"""
        self.__config = config
        self.__hs = habitica_service

    @classmethod
    def get_arg_parser(cls):
        """Gets the argument parser containing Utility function CLI arguments.

        Returns: argparse.ArgParser:  The ArgParser containing the argument
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
            '-t',
            '--test',
            required=False,
            action='store_true',
            help='''Run the current test function''')

        return parser

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

    def set_health(self, hp):
        """Sets the user health to the specified value"""
        old_hp = self.__hs.get_stats()['hp']
        new_hp = self.__hs.set_hp(hp)
        logging.getLogger(__name__).info(
            'HP changed from %f to %f',
            old_hp,
            new_hp)

    def set_xp(self, xp):
        """Sets the user experience points to the specified value"""
        old_xp = self.__hs.get_stats()['exp']
        new_xp = self.__hs.set_exp(xp)
        logging.getLogger(__name__).info(
            'XP changed from %f to %f',
            old_xp,
            new_xp)

    def set_mana(self, mp):
        """Sets the user mana to the specified value"""
        old_mp = self.__hs.get_stats()['mp']
        new_mp = self.__hs.set_mp(mp)
        logging.getLogger(__name__).info(
            'MP changed from %f to %f',
            old_mp,
            new_mp)

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

    def __test(self):
        """A test function. Could do anything depending on what I am testing."""
        print()
        logging.getLogger(__name__).debug('Running test function')
        print("--------------------")
        print("--------------------")
        print()
