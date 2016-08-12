# -*- coding: utf-8 -*-
""" Synchronisation of Trello cards to Habitica To-Dos.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging
import os
from configparser import ConfigParser
from pprint import pprint

import scriptabit
from trello import TrelloClient
from trello.util import create_oauth_token

class Trello(scriptabit.IPlugin):
    """ Trello card synchronisation.

    Attributes:
        __config: ConfigParser instance
        __tc: TrelloClient instance
    """

    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()
        self.__config = None
        self.__tc = None

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Note that to avoid argument name conflicts, only long argument names
        should be used, and they should be prefixed with the plugin-name or
        unique abbreviation.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        # Boards to sync (empty list for all active boards)
        parser.add(
            '--trello-boards',
            required=False,
            action='append',
            help='''The list of Trello boards to sync. Leave empty to
sync all active boards''')

        # Lists to sync (empty list for all lists in all selected boards)
        parser.add(
            '--trello-lists',
            required=False,
            action='append',
            help='''The Trello lists to sync. Leave empty to
sync all lists on all selected boards''')

        # Lists that mark cards as done
        parser.add(
            '--trello-done-lists',
            required=False,
            action='append',
            help='''The Trello lists that mark cards as complete.
If empty, then cards are only marked done when archived.''')

        return parser

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Generally, any initialisation should be done here rather than in
        activate or __init__.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """
        super().initialise(configuration, habitica_service)

        logging.getLogger(__name__).info(
            'Syncing Trello boards %s',
            configuration.trello_boards)

        logging.getLogger(__name__).info(
            'Syncing Trello lists %s',
            configuration.trello_lists)

        logging.getLogger(__name__).info(
            'Trello done lists %s',
            configuration.trello_done_lists)

        credentials = self.__load_authentication_credentials()

        if not credentials['token'] or not credentials['tokensecret']:
            logging.getLogger(__name__).warning('Getting Trello OAuth token')
            access_token = create_oauth_token(
                expiration='never',
                scope='read,write',
                key=credentials['apikey'],
                secret=credentials['apisecret'],
                name='scriptabit',
                output=True)
            credentials['token'] = access_token['oauth_token']
            credentials['tokensecret'] = access_token['oauth_token_secret']

            # Write back to the file
            config_file_path = os.path.join(
                os.path.expanduser("~"),
                '.auth.cfg')
            with open(config_file_path, 'w') as f:
                logging.getLogger(__name__).warning(
                    'Writing Trello OAuth tokens back to .auth.cfg')
                self.__config.set('trello', 'token', credentials['token'])
                self.__config.set(
                    'trello',
                    'tokensecret',
                    credentials['tokensecret'])
                self.__config.write(f)

        # we are finished with the configparser now
        self.__config = None

        # Instantiate the Trello Client
        self.__tc = TrelloClient(
            api_key=credentials['apikey'],
            api_secret=credentials['apisecret'],
            token=credentials['token'],
            token_secret=credentials['tokensecret'])

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        return 30

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        # logging.getLogger(__name__).info('')

        # pprint(dir(self.__tc))
        boards = self.__tc.list_boards()
        for b in boards:
            print('name: ', b.name)
            print('closed: ', b.closed)

        pprint(dir(boards[0]))

        # return False if finished, and True to be updated again.
        return False

    def __load_authentication_credentials(
            self,
            config_file_name='.auth.cfg',
            section='trello'):
        """ Loads authentication credentials from an ini-style
        configuration file.

        Args:
            config_file_name (str): Basename of the configuration file.
            section (str): Configuration file section name.

        Returns: dict: the selected credentials
        """
        config_file_path = os.path.join(
            os.path.expanduser("~"),
            config_file_name)

        logging.getLogger(__name__).info(
            "Loading trello credentials from %s",
            config_file_path)

        if not os.path.exists(config_file_path):
            raise scriptabit.ConfigError(
                "File '{0}' not found".format(config_file_path))

        self.__config = ConfigParser()
        self.__config.read(config_file_path)

        credentials = {}
        credentials['apikey'] = self.__config.get(section, 'apikey')
        credentials['apisecret'] = self.__config.get(section, 'apisecret')
        credentials['token'] = self.__config.get(section, 'token')
        credentials['tokensecret'] = self.__config.get(section, 'tokensecret')

        return credentials
