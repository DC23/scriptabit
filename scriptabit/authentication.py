# -*- coding: utf-8 -*-
""" Authentication credential loading functions
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import os
from configparser import ConfigParser, NoSectionError, NoOptionError
from .errors import ConfigError

def load_authentication_credentials(
        config_file_path='~/.auth.cfg',
        section='Habitica'):
    """ Loads authentication credentials from an ini-style configuration file.

    Args:
        config_file_path (str): Path to the configuration file.
        section (str): Configuration file section name.

    Returns: dict: the selected credentials::

        {
            'x-api-user': 'the user name',
            'x-api-key':  'the user API key',
        }

    Raises:
        ConfigError: specified file section or options are missing
    """

    credentials = {}
    config_file_path = os.path.expandvars(os.path.expanduser(config_file_path))

    if not os.path.exists(config_file_path):
        raise ConfigError("File '{0}' not found".format(config_file_path))

    config = ConfigParser()
    config.read(config_file_path)

    try:
        credentials = {
            'x-api-user': config.get(section, 'userid'),
            'x-api-key': config.get(section, 'apikey')
        }
    except NoSectionError:
        raise ConfigError("No '{0}' section in '{1}'".format(
            section, config_file_path))
    except NoOptionError as error:
        raise ConfigError("Missing option in auth file '{0}': {1}".format(
            config_file_path, error.message))

    return credentials
