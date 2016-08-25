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
import logging
import os
from configparser import ConfigParser, NoSectionError, NoOptionError
from .configuration import copy_default_config_to_user_directory
from .errors import ConfigError


def load_habitica_authentication_credentials(
        config_file_name='.auth.cfg',
        section='habitica'):
    """ Loads authentication credentials from an ini-style configuration file.

    Args:
        config_file_name (str): Basename of the configuration file.
        section (str): Configuration file section name.

    Returns:
        dict: the selected credentials

    .. code-block:: python

            {
            'x-api-user': 'the user name',
            'x-api-key':  'the user API key',
            }

    Raises:
        ConfigError: specified file section or options are missing
        """

    config_file_path = os.path.join(
        os.path.expanduser("~"),
        config_file_name)

    logging.getLogger(__name__).info("Loading credentials from %s",
                                     config_file_path)

    if not os.path.exists(config_file_path):
        logging.getLogger(__name__).warning("%s not found. Creating default",
                                            config_file_path)
        copy_default_config_to_user_directory(
            basename='.auth.cfg',
            clobber=False,
            dst_dir='~')
        raise ConfigError("File '{0}' not found".format(config_file_path))

    config = ConfigParser()
    config.read(config_file_path)

    try:
        x_api_user = config.get(section, 'userid')
        x_api_key = config.get(section, 'apikey')

        if not x_api_user:
            raise ConfigError("userid value in '{0}' is empty".format(
                config_file_path))
        if not x_api_key:
            raise ConfigError("apikey value in '{0}' is empty".format(
                config_file_path))

        return {
            'x-api-user': x_api_user,
            'x-api-key': x_api_key,
        }
    except NoSectionError:
        raise ConfigError("No '{0}' section in '{1}'".format(
            section, config_file_path))
    except NoOptionError as error:
        raise ConfigError("Missing option in auth file '{0}': {1}".format(
            config_file_path, error.message))
