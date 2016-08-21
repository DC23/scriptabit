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

        tasks = []
        tag_names = []
        row_count = 0

        with open(self._config.csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row_count += 1  # OK to do this first, as we skip the header
                    task = {
                        'text': row['name'],
                        'notes': row['description'],
                        'type': row['type'],
                        # TODO: due_date
                    }

                    task['priority'] = self.__parse_enum(
                        Difficulty,
                        row['difficulty'])

                    task['attribute'] = self.__parse_enum(
                        CharacterAttribute,
                        row['attribute'])

                    if task['type'] == 'habit':
                        task['up'] = self.__parse_bool(row['up'])
                        task['down'] = self.__parse_bool(row['down'])

                    if row['tags']:
                        tags = row['tags'].split(',')
                        tag_names += tags
                        task['tags'] = tags  # placeholder, filled in later

                    if task['type'] in ['habit', 'daily', 'todo', 'reward']:
                        tasks.append(task)
                    else:
                        logging.getLogger(__name__).warn(
                            'Skipping task on row %d: type not specified',
                            row_count)

                except Exception as exception:
                    logging.getLogger(__name__).error(exception, exc_info=True)

        if tag_names:
            tag_names = list(set(tag_names))  # remove duplicates

            if self._config.dry_run:
                print()
                pprint(tag_names)
            else:
                tags = self._hs.create_tags(tag_names)
                for task in tasks:
                    # replace the placeholder names with tag IDs
                    n = task.get('tags', None)
                    if n:
                        task['tags'] = [t['id'] for t in tags if t['name'] in n]

        logging.getLogger(__name__).info('Processed %d rows', row_count)

        if self._config.dry_run:
            pprint(tasks)
        else:
            result = self._hs.create_tasks(tasks)
            pprint(result)

        # return False if finished, and True to be updated again.
        return False

    def __parse_bool(self, csv_value):
        """parse a bool from a string value"""
        if not csv_value or csv_value.lower() == 'false':
            return 'false'
        return 'true'

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
