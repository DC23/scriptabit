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
import pprint

import iso8601


class UtilityFunctions(object):
    """Runs the CLI-selected scriptabit utility functions.
    These are a collection of single-shot functions that get executed outside
    the primary scenario scripting framework.
    """

    __config = None
    __hs = None

    # TODO: can I move the definition of the utility CLI args to this class?
    def __init__(self, config, habitica_service):

        logging.getLogger(__name__).info('UtilityFunctions online')
        self.__config = config
        self.__hs = habitica_service

    def run(self):
        """Runs the user-selected scriptabit utility functions"""

        if self.__config.show_user_data:
            self.show_user_data()

    def show_user_data(self):
        """Shows the user data"""

        logging.getLogger(__name__).debug('Getting user data')
        data = self.__hs.get_user()

        print()
        print("Summarised User Data")
        print("--------------------")
        print()

        print(data['profile']['name'])

        print("Last Cron: {0}".format(
            iso8601.parse_date(data['lastCron']).astimezone()))

        pprint.pprint(data['stats'])

        print("--------------------")
        print()
