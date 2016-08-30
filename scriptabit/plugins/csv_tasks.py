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
        self.tasks = []
        self.tag_names = []
        self.__print_help = None

    @staticmethod
    def supports_dry_runs():
        """ The CSV plugin supports dry runs.

        Returns:
            bool: True
        """
        return True

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

        self.__print_help = parser.print_help

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

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        if not self._config.csv_file:
            logging.getLogger(__name__).warning('No CSV file specified')
            self.__print_help()
            return False

        logging.getLogger(__name__).info(
            'Importing tasks from %s',
            self._config.csv_file)

        row_count = 0

        with open(self._config.csv_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    row_count += 1  # OK to do this first, as we skip the header
                    task = {
                        'text': row['name'],
                        'type': row['type'],
                    }
                    # TODO: due_date

                    if 'description' in row.keys():
                        task['notes'] = row['description']

                    if 'priority' in row.keys():
                        task['priority'] = self.__parse_enum(
                            Difficulty,
                            row['difficulty'])

                    if 'attribute' in row.keys():
                        task['attribute'] = self.__parse_enum(
                            CharacterAttribute,
                            row['attribute'])

                    if task['type'] == 'habit':
                        task['up'] = self.__parse_bool(row['up'])
                        task['down'] = self.__parse_bool(row['down'])

                    if task['type'] == 'reward' and 'value' in row.keys():
                        task['value'] = max(0, int(row['value']))

                    if 'tags' in row.keys():
                        if row['tags']:
                            tags = row['tags'].split(',')
                            self.tag_names += tags
                            task['tags'] = tags  # placeholder, filled in later

                    if task['type'] in ['habit', 'daily', 'todo', 'reward']:
                        self.tasks.append(task)
                    else:
                        logging.getLogger(__name__).warning(
                            'Skipping task on row %d: invalid task type',
                            row_count)

                except ValueError as ex:
                    logging.getLogger(__name__).error(ex, exc_info=True)
                except KeyError as ex:
                    logging.getLogger(__name__).error(ex, exc_info=True)
                except Exception as ex:
                    logging.getLogger(__name__).error(ex, exc_info=True)

        self.__fill_tag_placeholders()

        if not self.tasks:
            logging.getLogger(__name__).warning(
                'No tasks created. Check your CSV file format')
            return False

        if not self.dry_run and self.tasks:
            self._hs.create_tasks(self.tasks)

        self.__notify('Uploaded {0} rows from CSV'.format(row_count))

        # return False if finished, and True to be updated again.
        return False

    def __fill_tag_placeholders(self):
        """Replace tag name placeholders with tag IDs"""
        if self.tag_names:
            self.tag_names = list(set(self.tag_names))  # remove duplicates

            if self._config.dry_run:
                print()
                pprint(self.tag_names)
            else:
                tags = self._hs.create_tags(self.tag_names)
                for task in self.tasks:
                    # replace the placeholder names with tag IDs
                    n = task.get('tags', None)
                    if n:
                        task['tags'] = [t['id'] for t in tags if t['name'] in n]

    @staticmethod
    def __parse_bool(csv_value):
        """parse a bool from a string value"""
        if not csv_value or csv_value.lower() == 'false':
            return 'false'
        return 'true'

    @staticmethod
    def __parse_enum(enum, name):
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

    def __notify(self, message):
        """ Notify the Habitica user """
        logging.getLogger(__name__).info(message)
        if not self.dry_run:
            scriptabit.UtilityFunctions.upsert_notification(
                self._hs,
                text=message)
