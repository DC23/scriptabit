# -*- coding: utf-8 -*-
""" Bulk creation of Habitica tasks from CSV files.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import csv
import logging
from pprint import pprint

import scriptabit
from scriptabit import CharacterAttribute, Difficulty

class CsvTasks(scriptabit.IPlugin):
    """ Scriptabit batch CSV task importer for Habitica
    """
    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Note that to avoid argument name conflicts, only long argument names
        should be used, and they should be prefixed with the plugin-name or
        unique abbreviation.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--csv-file',
            required=False,
            metavar='FILE',
            help='CSV file for bulk task import')

        return parser

    def activate(self):
        """ Called by the plugin framework when a plugin is activated."""
        pass

    def deactivate(self):
        """ Called by the plugin framework when a plugin is deactivated."""
        pass

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the plugin.

        Generally, any initialisation should be done here rather than in
        activate or __init__.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        super().initialise(configuration, habitica_service, data_dir)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        # minimum update frequency of once every 1 minute, or whatever the
        # user specified
        return max(1, self._config.update_frequency)

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        logging.getLogger(__name__).info(
            'Importing tasks from %s',
            self._config.csv_file)

        with open(self._config.csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                print()
                pprint(row)
                try:
                    task = {
                        'text': row['name'],
                        'notes': row['description'],
                        'type': row['type'],
                        # TODO: due_date
                        # TODO: up if habit
                        # TODO: down if habit
                    }

                    task['priority'] = self.__parse_enum(
                        Difficulty,
                        row['difficulty'])

                    task['attribute'] = self.__parse_enum(
                        CharacterAttribute,
                        row['attribute'])

                    # TODO: tags are harder than might be apparent, but I have
                    # code to help

                    if self._config.dry_run:
                        pprint(task)
                    else:
                        self._hs.create_task(task)

                except Exception as exception:
                    logging.getLogger(__name__).error(exception, exc_info=True)

        # return False if finished, and True to be updated again.
        return False

    def __parse_enum(self, enum, name):
        """ Parse an enum, trying both lookup by name and value.
            Returns the default if neither lookup succeeds.
        """
        value = enum.default.value
        try:
            value = enum[name].value
        except:
            try:
                value = enum.from_value(name).value
            except:
                pass
        return value
