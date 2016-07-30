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


class UtilityFunctions(object):
    """Runs the user-selected scriptabit utility functions"""

    __config = None
    __hs = None

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
        pprint.pprint(data)
