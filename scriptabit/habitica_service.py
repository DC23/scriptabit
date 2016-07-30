# -*- coding: utf-8 -*-
""" Thin and minimal Habitica API service interface.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import logging


class HabiticaService(object):
    """ Thin and minimal Habitica API service interface.  """

    __http_service = None
    __headers = {}
    __base_url = ''

    def __init__(self, http_service, headers, base_url):
        """
        Args:
            http_service: A HTTP service with a requests-like interface.
            headers: HTTP headers.
            base_url: The base URL for requests.
        """

        self.__http_service = http_service
        self.__headers = headers
        self.__base_url = base_url
        logging.getLogger(__name__).debug('HabiticaService online')

    def __get(self, command):
        """Utility wrapper around a HTTP get"""

        url = self.__base_url + command
        logging.getLogger(__name__).debug('GET %s', url)
        return self.__http_service.get(url, headers=self.__headers)

    def is_server_up(self):
        """Check that the Habitica API is reachable and up"""

        response = self.__get('status')
        if response.status_code == self.__http_service.codes.ok:
            return response.json()['data']['status'] == 'up'
        return False

    def get_user(self):
        """Get authenticated user data"""

        response = self.__get('user')
        if response.status_code == self.__http_service.codes.ok:
            return response.json()['data']
        return None
