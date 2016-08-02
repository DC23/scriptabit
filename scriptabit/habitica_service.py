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


class HabiticaService(object):
    """ Habitica API service interface.  """

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
        """Utility wrapper around a HTTP get"""

        url = self.__base_url + command
        logging.getLogger(__name__).debug('GET %s', url)
        return requests.get(url, headers=self.__headers)

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

        Returns: dictionary: a raw dictionary mapped directly from the JSON API
        response.
        """

        response = self.__get('user')
        if response.status_code == requests.codes.ok:
            return response.json()['data']
        return None
