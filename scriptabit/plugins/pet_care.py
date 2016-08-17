# -*- coding: utf-8 -*-
""" Habitica pet care.

Options for batch hatching and feeding pets.
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

import scriptabit

class PetCare(scriptabit.IPlugin):
    """ Habitica pet care
    """

    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()
        self.__items = None
        self.__print_help = None

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--pets-list-items',
            required=False,
            action='store_true',
            help='Lists all pet-related items')

        self.__print_help = parser.print_help

        return parser

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
        logging.getLogger(__name__).info('Scriptabit Pet Care Services: looking'
                                         ' after your pets since yesterday')

        self.__items = self._hs.get_user()['items']

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        return 2.0 / 60.0  # 2 seconds

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """

        # do work here
        if self._config.pets_list_items:
            self.__list_pet_items(self.__items)
            return False

        self.__print_help()

        # return False if finished, and True to be updated again.
        return False

    @staticmethod
    def __list_pet_items(items):
        """ Lists all pet-related inventory items.

        Args:
            items (dict): The Habitica user.items dictionary.
        """
        print()
        print('Eggs:')
        pprint(items['eggs'])
        print()
        print('Hatching potions:')
        pprint(items['hatchingPotions'])
        print()
        print('Food:')
        pprint(items['food'])
        print()
        print('Pets:')
        pprint(items['pets'])
        print()
        print('Mounts:')
        pprint(items['mounts'])
