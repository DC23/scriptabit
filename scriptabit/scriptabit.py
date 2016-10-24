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
import os
from datetime import datetime
from time import sleep

from pkg_resources import Requirement, resource_filename
from yapsy.PluginManager import PluginManager

from .authentication import load_habitica_authentication_credentials
from .configuration import (
    get_configuration,
    get_config_file,
    copy_default_config_to_user_directory)
from .errors import ServerUnreachableError, PluginError
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

def __get_configuration(plugin_manager):
    """ Builds and parses the hierarchical configuration from environment
    variables, configuration files, command-line arguments,
    and argument defaults.

    Args:
        plugin_manager (yapsy.PluginManager): The plugin manager.

    Returns:
        The argparse compatible configuration object.
    """

    extra_args = [UtilityFunctions.get_arg_parser()]

    # Plugins can define additional arguments
    for plugin_info in plugin_manager.getAllPlugins():
        plugin_arg_parser = plugin_info.plugin_object.get_arg_parser()
        extra_args.append(plugin_arg_parser)

    config, _ = get_configuration(parents=extra_args)

    return config

def __init_user_plugin_directory():
    """ Locates (and creates if necessary) the user plugin directory. """
    default = os.path.expanduser('~/scriptabit_plugins')
    user = os.path.expanduser(os.getenv('SCRIPTABIT_USER_PLUGIN_DIR', ''))
    plugin_dir = user if user else default

    if not os.path.exists(plugin_dir):
        # Can't use logging, as logging is initialised after plugins
        print('Creating user plugin directory {0}'.format(plugin_dir))
        os.makedirs(plugin_dir)

    return plugin_dir

def __get_plugin_manager():
    """ Discovers and instantiates all plugins, returning a management object.

    Returns:
        yapsy.PluginManager: The plugin manager with the loaded plugins.
    """
    # Build the manager
    plugin_manager = PluginManager()

    # the location of the plugins that ship with scriptabit
    package_plugin_path = resource_filename(
        Requirement.parse("scriptabit"),
        os.path.join('scriptabit', 'plugins'))

    # user plugin location
    user_plugin_path = __init_user_plugin_directory()

    # Set plugin locations
    plugin_manager.setPluginPlaces([package_plugin_path, user_plugin_path])

    # Load all plugins
    plugin_manager.collectPlugins()

    return plugin_manager

def __list_plugins(plugin_manager):
    """ Lists the available plugins.

    Args:
        plugin_manager (yapsy.PluginManager): the plugin manager containing
        the plugins.
    """
    def print_plugin_metadata(plugin_info):
        """Utility class to pretty-print plugin information."""

        print('* {0}:'.format(plugin_info.name))
        print('{0}'.format(plugin_info.description))

    print()
    print('---- Plugins ----')
    print('To execute a plugin, use the plugin name with the -r argument.')
    print()
    for plugin_info in plugin_manager.getAllPlugins():
        print_plugin_metadata(plugin_info)
        print()
    print('-----------------')
    print()

def __init_config_and_plugin_manager():
    """ Initialises the configuration and plugin manager for all entry points.

    Returns:
        config: The program configuration.
        plugin_manager: The plugin manager.
    """
    plugin_manager = __get_plugin_manager()
    config = __get_configuration(plugin_manager)
    return config, plugin_manager

def start_scriptabit():
    """ Command-line entry point for scriptabit """
    run_scriptabit()

def start_banking():
    """ Command-line entry point for banking """
    run_scriptabit('banking')

def start_csv():
    """ Command-line entry point for csv """
    run_scriptabit('csv_tasks')

def start_health():
    """ Command-line entry point for health """
    run_scriptabit('health_effects')

def start_pets():
    """ Command-line entry point for pets """
    run_scriptabit('pet_care')

def start_trello():
    """ Command-line entry point for Trello """
    run_scriptabit('trello')

def run_scriptabit(plugin_name=''):
    """ Runs scriptabit.

    Args:
        plugin_name (str): The optional plugin. If supplied, then this plugin is
            executed regardless of the actual command line arguments.
    """
    config, plugin_manager = __init_config_and_plugin_manager()

    if plugin_name:
        config.run = plugin_name

    __init_logging(config.logging_config)
    logging.getLogger(__name__).info('scriptabit version %s', __version__)

    if config.version:
        return

    try:
        if config.list_plugins:
            logging.getLogger(__name__).debug('Listing available plugins')
            __list_plugins(plugin_manager)
        else:
            # --------------------------------------------------
            # Running against Habitica.
            # Get everything warmed up and online.
            # --------------------------------------------------

            # user credentials
            auth_tokens = load_habitica_authentication_credentials(
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

            if not config.run:
                # Utility functions
                utility = UtilityFunctions(config, habitica_service)
                utility.run()
            else:
                # Time to run the selected plugin
                # First, find it
                logging.getLogger(__name__).info("** %s running", config.run)
                print()

                plugin_info = plugin_manager.getPluginByName(config.run)

                if not plugin_info:
                    raise PluginError('plugin %s not found' % config.run)

                # Second, activate it
                plugin_manager.activatePluginByName(config.run)
                plugin = plugin_info.plugin_object

                if config.dry_run:
                    if not plugin.supports_dry_runs():
                        raise PluginError('Dry run mode not supported')

                    logging.getLogger(__name__).info(
                        'Dry run mode: no changes will be written')

                data_dir = __init_user_plugin_directory()
                logging.getLogger(__name__).debug(
                    'User plugin and data directory: %s', data_dir)
                plugin.initialise(config, habitica_service, data_dir)

                # Finally, run it
                updating = True
                count = 0

                def keep_updating():
                    """ Test for whether another update is required """
                    return (
                        updating and not
                        (config.max_updates > 0 and
                         count >= config.max_updates))

                while keep_updating():
                    logging.getLogger(__name__).info(
                        "%s update %d @ %s",
                        config.run, count, datetime.now().strftime("%c"))

                    try:
                        updating = plugin.update()
                    except Exception as e:
                        logging.getLogger(__name__).error(
                            'Plugin Update failed')
                        logging.getLogger(__name__).error(e, exc_info=True)

                    count += 1

                    # Only sleep if we have another update pending
                    if keep_updating():
                        logging.getLogger(__name__).info(
                            "Sleeping for %f minutes",
                            plugin.update_interval_minutes())
                        sleep(plugin.update_interval_seconds())

                print()
                logging.getLogger(__name__).info("** %s done", config.run)

    except Exception as exception:
        logging.getLogger(__name__).error(exception, exc_info=True)

    logging.getLogger(__name__).info("Exiting")


if __name__ == 'main':
    start_scriptabit()
