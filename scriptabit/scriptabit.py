# -*- coding: utf-8 -*-
""" Scriptabit: Python scripting for Habitica.
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
from .configuration import (
    get_configuration,
    get_config_file,
    copy_default_config_to_user_directory,
)
from .errors import ServerUnreachableError
from .habitica_service import HabiticaService
from .metadata import __version__
from .utility_functions import UtilityFunctions


def __init_logging(logging_config_file):
    """
    Initialises logging.

    Args:
        logging_config_file (str): The logging configuration file.
        """

    # Make sure the user copy of the logging config file exists
    copy_default_config_to_user_directory(logging_config_file, clobber=False)

    # Load the config
    logging.config.fileConfig(get_config_file(logging_config_file))
    logging.getLogger(__name__).debug('Logging online')


def start_cli():
    """ Command-line entry point for scriptabit """

    # TODO: build a list of available scenarios
    # TODO: give all scenarios a chance to add new configuration options
    config, _ = get_configuration()
    __init_logging(config.logging_config)

    logging.getLogger(__name__).info('scriptabit version %s', __version__)

    # Disabling the broad exception warning as catching
    # everything is *exactly* the intent here.
    # pylint: disable=broad-except
    try:
        if config.list_scenarios:
            logging.getLogger(__name__).debug('Listing available scenarios')
        else:
            # --------------------------------------------------
            # Running against Habitica.
            # Get everything warmed up and online.
            # --------------------------------------------------

            # user credentials
            auth_tokens = load_authentication_credentials(
                section=config.auth_section)

            # Habitica Service
            habitica_service = HabiticaService(
                auth_tokens,
                config.habitica_api_url)

            # Test for server availability
            if not habitica_service.is_server_up():
                raise ServerUnreachableError(
                    "Habitica API at '{0}' is unreachable or down".format(
                        config.habitica_api_url))

            logging.getLogger(__name__).info("Habitica API at '%s' is up",
                                             config.habitica_api_url)

            # Utility functions
            utility = UtilityFunctions(config, habitica_service)
            utility.run()

            if config.scenario:
                # Time to run the selected scenario
                logging.getLogger(__name__).debug(
                    "Running '%s' scenario", config.scenario)

                # TODO: scenario factory and execution
    except Exception as exception:
        logging.getLogger(__name__).error(exception, exc_info=True)
        # pylint: enable=broad-except

    logging.getLogger(__name__).info("Exiting")


if __name__ == 'main':
    start_cli()
