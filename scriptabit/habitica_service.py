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

from .errors import *


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

    def __post(self, command, data):
        """Utility wrapper around a HTTP POST"""
        url = self.__base_url + command
        logging.getLogger(__name__).debug('PUT %s', url)
        return requests.post(url, headers=self.__headers, data=data)

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
        response.raise_for_status()
        return response.json()['data']

    def get_stats(self):
        """Gets the authenticated user stats.

        Returns: dictionary: The stats.
        """
        return self.get_user()['stats']

    def get_tasks(self):
        """Gets all tasks for the current user.

        Returns: dictionary: The tasks.
        """
        response = self.__get('tasks/user')
        response.raise_for_status()
        return response.json()['data']

    def create_task(self, task):
        """ Creates a task.

        Args:
            task (dict): The task.

        Returns: dict: The new task as returned from the server.
        """
        response = self.__post('tasks/user', task)
        response.raise_for_status()
        return response.json()['data']

    def get_task(self, _id='', alias=''):
        """ Gets a task.

        If both task ID and alias are specified, then the ID is used.

        Args:
            _id (str): The task ID.
            alias (str): The task alias.

        Returns: dict: The task, or None if the task is not found.

        Raises:
            ValueError
        """
        key = _id if _id else alias
        if not key:
            raise ValueError('Neither ID or alias specified')

        response = self.__get('tasks/{key}'.format(key=key))
        if response.status_code == requests.codes.ok:
            return response.json()['data']
        else:
            return None

    def upsert_task(self, task):
        """Upserts a task.

        Existing tasks will be updated, otherwise a new task will be created.

        Args:
            task (dict): The task.

        Returns: dict: The new task as returned from the server.

        Raises:
            ValueError
        """
        key = task['_id'] if '_id' in task else task.get('alias', None)
        if not key:
            raise ValueError(
                'The task must specify an id or alias')

        # Does the task already exist?
        if self.get_task(key):
            logging.getLogger(__name__).debug('task %s exists, updating', key)
            response = self.__put('tasks/{0}'.format(key), task)
            response.raise_for_status()
            return response.json()['data']
        else:
            logging.getLogger(__name__).debug(
                'task %s not found, creating', key)
            self.create_task(task)

    # TODO: I don't think the API lets me set partial user objects in this way.
    # So I could get the entire user structure, swap the stats for the argument
    # version, and then PUT that back. Or I can wait to see if I even need this
    # method at all.
    # def set_stats(self, stats):
    # """Sets the authenticated user stats.
    # ** Not implemented **
    # Note that unlike the fine-grained set_[hp|mp|xp] methods,
    # this method performs no sanity checking of values.

        # Args:
        # stats (dict): The stats to set. This can be a
        # partial set of values.

        # Returns: dictionary: The new stats, as returned by the server.

        # Raises: NotImplementedError
        # """
        # raise NotImplementedError
        # response = self.__put('user', {'stats': stats})
        # if response.status_code == requests.codes.ok:
        # return response.json()['data']['stats']
        # return None

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
        response.raise_for_status()
        return response.json()['data']['stats']['hp']

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
        response.raise_for_status()
        return response.json()['data']['stats']['mp']

    def set_exp(self, exp):
        """ Sets the user's XP (experience points).

        Args:
            exp (float): The new XP value.

        Returns: float: The new XP value, extracted from the JSON response data.
        """
        if exp < 0:
            raise ArgumentOutOfRangeError("exp < 0")

        response = self.__put('user', {'stats.exp': exp})
        response.raise_for_status()
        return response.json()['data']['stats']['exp']

    def set_gp(self, gp):
        """ Sets the user's gold (gp).

        Args:
            gp (float): The new gold value.

        Returns: float: The new gold value, extracted from the response data.
        """
        if gp < 0:
            raise ArgumentOutOfRangeError("gp < 0")

        response = self.__put('user', {'stats.gp': gp})
        response.raise_for_status()
        return response.json()['data']['stats']['gp']
