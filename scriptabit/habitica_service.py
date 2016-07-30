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
import requests

# Disable some pylint errors caused by perfectly correct use of requests
# pylint: disable=invalid-name
# pylint: disable=no-member

def __get(base_url, command, headers):
    """Utility wrapper around a get"""

    return requests.get(base_url+command, headers=headers)

def is_server_up(base_url='https://habitica.com/api/v3/'):
    """Check that the Habitica API is reachable and up"""

    url = base_url + '/status'
    logging.getLogger(__name__).debug(url)
    r = requests.get(base_url+'/status')
    if r.status_code == requests.codes.ok:
        return r.json()['data']['status'] == 'up'
    return False
