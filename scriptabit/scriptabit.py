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

from .configuration import __get_configuration
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
            logging.getLogger(__name__).info('Listing available scenarios')
        elif config.scenario:
            logging.getLogger(__name__).info(
                "Running '%s' scenario", config.scenario)
            # TODO: scenario factory and execution
        else:
            print_help()
    except Exception as exception:
        logging.getLogger(__name__).error(exception, exc_info=True)
    # pylint: enable=broad-except


if __name__ == 'main':
    start_cli()
