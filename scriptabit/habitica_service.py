# -*- coding: utf-8 -*-
""" Habitica API service interface.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import logging
import requests

from .errors import ArgumentOutOfRangeError


class HabiticaService(object):
    """ Habitica API service interface. """

    __headers = {}
    __base_url = ''

    def __init__(self, headers, base_url):
        """
        Args:
            headers: HTTP headers.
            base_url: The base URL for requests.
            """

        self.__headers = headers
        self.__base_url = base_url
        logging.getLogger(__name__).debug('HabiticaService online')

    def __get(self, command):
        """Utility wrapper around a HTTP GET"""

        url = self.__base_url + command
        logging.getLogger(__name__).debug('GET %s', url)
        return requests.get(url, headers=self.__headers)

    def __put(self, command, data):
        """Utility wrapper around a HTTP PUT"""

        url = self.__base_url + command
        logging.getLogger(__name__).debug('PUT %s', url)
        return requests.put(url, headers=self.__headers, data=data)

    def is_server_up(self):
        """Check that the Habitica API is reachable and up

        Returns: bool: `True` if the server is reachable, otherwise `False`.
        """

        response = self.__get('status')
        if response.status_code == requests.codes.ok:
            return response.json()['data']['status'] == 'up'
        return False

    def get_user(self):
        """Gets the authenticated user data.

        Returns: dictionary: The user data.
        """

        response = self.__get('user')
        if response.status_code == requests.codes.ok:
            return response.json()['data']
        return None

    def get_user_stats(self):
        """Gets the authenticated user stats.

        Returns: dictionary: The user stats.
        """

        return self.get_user()['stats']

    def set_user_stats(self, stats):
        """Sets the authenticated user stats.

        Args:
            stats (dict): The user stats to set. This can be a
            partial set of values.

        Returns: dictionary: The new user stats, as returned by the server.
        """

        response = self.__put('user', {'stats': stats})
        if response.status_code == requests.codes.ok:
            return response.json()['data']['stats']
        return None

    def set_hp(self, hp):
        """ Sets the user's HP.

        Args:
            hp (float): The new HP value.

        Returns: float: The new HP value, extracted from the JSON response data.
        """

        if hp > 50:
            raise ArgumentOutOfRangeError("hp > 50")
        if hp < 0:
            raise ArgumentOutOfRangeError("hp < 0")

        response = self.__put('user', {'stats.hp': hp})
        if response.status_code == requests.codes.ok:
            return response.json()['data']['stats']['hp']
        return None

    def set_mp(self, mp):
        """ Sets the user's MP (mana points).

        Args:
            mp (float): The new MP value.

        Returns: float: The new MP value, extracted from the JSON response data.
        """

        max_mp = self.get_user()['stats']['mp']
        if mp > max_mp:
            raise ArgumentOutOfRangeError("mp > {0}".format(max_mp))
        if mp < 0:
            raise ArgumentOutOfRangeError("mp < 0")

        response = self.__put('user', {'stats.mp': mp})
        if response.status_code == requests.codes.ok:
            return response.json()['data']['stats']['mp']
        return None

    def set_exp(self, exp):
        """ Sets the user's XP (experience points).

        Args:
            exp (float): The new XP value.

        Returns: float: The new XP value, extracted from the JSON response data.
        """

        if exp < 0:
            raise ArgumentOutOfRangeError("exp < 0")

        response = self.__put('user', {'stats.exp': exp})
        if response.status_code == requests.codes.ok:
            return response.json()['data']['stats']['exp']
        return None
