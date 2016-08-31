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
import os
import shutil
from string import Template

import configargparse
from pkg_resources import Requirement, resource_filename


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

def get_config_file(basename):
    """ Looks for a configuration file in 3 locations:

        - the current directory
        - the user config directory (~/.config/scriptabit)
        - the version installed with the package (using setuptools resource API)

    Args:
        basename (str): The base filename.

    Returns:
        str: The full path to the configuration file.
    """
    locations = [
        os.path.join(os.curdir, basename),
        os.path.join(
            os.path.expanduser("~"),
            ".config",
            "scriptabit",
            basename),
        resource_filename(
            Requirement.parse("scriptabit"),
            os.path.join('scriptabit', basename))
    ]

    for location in locations:
        if os.path.isfile(location):
            return location

def copy_default_config_to_user_directory(
        basename,
        clobber=False,
        dst_dir='~/.config/scriptabit'):
    """ Copies the default configuration file into the user config directory.

    Args:
        basename (str): The base filename.
        clobber (bool): If True, the default will be written even if a user
            config already exists.
        dst_dir (str): The destination directory.
    """
    dst_dir = os.path.expanduser(dst_dir)
    dst = os.path.join(dst_dir, basename)
    src = resource_filename(
        Requirement.parse("scriptabit"),
        os.path.join('scriptabit', basename))

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    if clobber or not os.path.isfile(dst):
        shutil.copy(src, dst)

def get_configuration(basename='scriptabit.cfg', parents=None):
    """Parses and returns the program configuration options,
    taken from a combination of ini-style config file, and
    command line arguments.

    Args:
        basename (str): The base filename.
        parents (list): A list of ArgumentParser objects whose arguments
            should also be included in the configuration parsing. These
            ArgumentParser instances **must** be instantiated with the
            `add_help` argument set to `False`, otherwise the main
            ArgumentParser instance will raise an exception due to duplicate
            help arguments.

    Returns:
        The options object, and a function that can be called to print the help
        text.
    """
    copy_default_config_to_user_directory(basename)

    parser = configargparse.ArgParser(
        formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter,
        parents=parents or [],
        default_config_files=[
            resource_filename(
                Requirement.parse("scriptabit"),
                os.path.join('scriptabit', basename)),
            os.path.join(
                os.path.expanduser("~/.config/scriptabit"),
                basename),
            os.path.join(os.curdir, basename)])

    # logging config file
    parser.add(
        '-lc',
        '--logging-config',
        required=False,
        default='scriptabit_logging.cfg',
        metavar='FILE',
        env_var='SCRIPTABIT_LOGGING_CONFIG',
        help='Logging configuration file')

    # Authentication file section
    parser.add(
        '-as',
        '--auth-section',
        required=False,
        default='habitica',
        help='''Name of the authentication file section containing the Habitica
credentials''')

    parser.add(
        '-url',
        '--habitica-api-url',
        required=False,
        default='https://habitica.com/api/v3/',
        help='''The base Habitica API URL''')

    # plugins
    parser.add(
        '-r',
        '--run',
        required=False,
        help='''Select the plugin to run. Note you can only run a single
plugin at a time. If you specify more than one, then only the
last one will be executed. To chain plugins together, create a
new plugin that combines the effects as required.''')

    parser.add(
        '-ls',
        '--list-plugins',
        required=False,
        action='store_true',
        help='''List available plugins''')

    parser.add(
        '-v',
        '--version',
        required=False,
        action='store_true',
        help='''Display scriptabit version''')

    parser.add(
        '-dr',
        '--dry-run',
        required=False,
        action='store_true',
        help='''Conduct a dry run. No changes are written to online services''')

    parser.add(
        '-n',
        '--max-updates',
        required=False,
        type=int,
        default=0,
        help='''If > 0, this sets a limit on the number of plugin updates.
Note that plugins can still exit before the limit is reached.''')

    parser.add(
        '-uf',
        '--update-frequency',
        required=False,
        type=int,
        default=-1,
        help='''If > 0, this specifies the preferred update frequency in minutes
for plugins that run in the update loop. Note that plugins may ignore or limit
this setting if the value is inappropriate for the specific plugin.''')

    return parser.parse_args(), parser.print_help
