# -*- coding: utf-8 -*-
""" Configuration and command-line arguments
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

from string import Template

import configargparse


def __add_min_max_value(
        parser,
        basename,
        default_min,
        default_max,
        initial,
        help_template):
    """
    Generates parser entries for options
    with a min, max, and default value.

    Args:
        parser: the parser to use.
        basename: the base option name. Generated options will have flags
            --basename-min, --basename-max, and --basename.
        default_min: the default min value
        default_max: the default max value
        initial: the default initial value
        help_template: the help string template.
            $mmi will be replaced with min, max, or initial.
            $name will be replaced with basename.
    """

    help_template = Template(help_template)

    parser.add(
        '--{0}-min'.format(basename),
        default=default_min,
        type=float,
        required=False,
        help=help_template.substitute(mmi='min', name=basename))

    parser.add(
        '--{0}-max'.format(basename),
        default=default_max,
        type=float,
        required=False,
        help=help_template.substitute(mmi='max', name=basename))

    parser.add(
        '--{0}'.format(basename),
        default=initial,
        type=float,
        required=False,
        help=help_template.substitute(mmi='initial', name=basename))


def get_configuration():
    """Parses and returns the program configuration options,
    taken from a combination of ini-style config file, and
    command line arguments.

    Returns:
        The options object, and a function that can be called to print the help
        text.
    """

    parser = configargparse.ArgParser(
        formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
        default_config_files=['./scriptabit.cfg'])

    # General options
    parser.add(
        '-c',
        '--config',
        required=False,
        is_config_file=True,
        default='scriptabit.cfg',
        metavar='FILE',
        help='scriptabit configuration file')

    # logging config file
    parser.add(
        '-lc',
        '--logging-config',
        required=False,
        default='scriptabit_logging.cfg',
        metavar='FILE',
        help='Logging configuration file')

    # authentication file location
    parser.add(
        '-af',
        '--auth-file',
        required=False,
        default='~/.auth.cfg',
        metavar='FILE',
        help='''Authentication file location''')

    # Authentication file section
    parser.add(
        '-as',
        '--auth-section',
        required=False,
        default='Habitica',
        help='''Name of the authentication file section containing the Habitica
        credentials''')

    parser.add(
        '-url',
        '--habitica-api-url',
        required=False,
        default='https://habitica.com/api/v3/',
        help='''The base Habitica API URL''')

    # Utility functions
    parser.add(
        '-sud',
        '--show-user-data',
        required=False,
        action='store_true',
        help='''Print the user data''')

    # Scenarios
    parser.add(
        '-s',
        '--scenario',
        required=False,
        help='''Select the scenario to run''')

    parser.add(
        '-ls',
        '--list-scenarios',
        required=False,
        action='store_true',
        help='''List available scenarios''')

    return parser.parse_args(), parser.print_help
