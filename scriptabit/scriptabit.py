# -*- coding: utf-8 -*-
""" Entry points for scriptabit
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import logging
import logging.config

from .authentication import load_authentication_credentials
from .configuration import __get_configuration
from .habitica_service import *
from .metadata import __version__


def __init_logging(logging_config_file):
    """
    Initialises logging.

    Args:
        logging_config_file (str): The logging configuration file.
        """

    logging.config.fileConfig(logging_config_file)
    logging.getLogger(__name__).debug('Logging online')


def start_cli():
    """ Command-line entry point for scriptabit """

    # TODO: build a list of available scenarios
    # TODO: give all scenarios a chance to add new configuration options
    config, print_help = __get_configuration()
    __init_logging(config.logging_config)

    logging.getLogger(__name__).info('scriptabit version %s', __version__)

    # Disabling the broad exception warning as catching
    # everything is *exactly* the intent here.
    # pylint: disable=broad-except
    try:
        if config.list_scenarios:
            logging.getLogger(__name__).debug('Listing available scenarios')

        elif config.scenario:

            # Test for server availability
            server_up = is_server_up(config.habitica_api_url)

            if not server_up:
                raise ServerUnreachableError(
                    "Habitica API at '%s' is unreachable or down" %
                    config.habitica_api_url)

            logging.getLogger(__name__).info(
                "Habitica API at '%s' is up" %
                config.habitica_api_url)

            # OK, server is reachable, get user's credentials
            logging.getLogger(__name__).debug('Loading credentials')
            auth_tokens = load_authentication_credentials(
                config.auth_file, config.auth_section)

            # Time to run the selected scenario
            logging.getLogger(__name__).debug(
                "Running '%s' scenario", config.scenario)

            # TODO: scenario factory and execution
        else:
            print_help()
    except Exception as exception:
        logging.getLogger(__name__).error(exception, exc_info=True)
        # pylint: enable=broad-except

    logging.getLogger(__name__).info("Exiting")


if __name__ == 'main':
    start_cli()
