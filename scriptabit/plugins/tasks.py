# -*- coding: utf-8 -*-
"""Task manipulation plugin
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
from time import sleep
from pprint import pprint
import logging

# from .dates import parse_date_local
# from .habitica_service import HabiticaTaskTypes, SpellIDs
import scriptabit as sb

class Tasks(sb.IPlugin):
    """ Tasks plugin implementation
    """
    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()
        self.task_type = None
        self.task_type_name = None

    @staticmethod
    def supports_dry_runs():
        """ Do we support dry runs?

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
            '--delete-tasks',
            required=False,
            action='store_true',
            help='''Delete all tasks''')

        parser.add(
            '--list-tasks',
            required=False,
            action='store_true',
            help='''List all tasks.''')

        parser.add(
            '--list-tags',
            required=False,
            action='store_true',
            help='''List all tags.''')

        parser.add(
            '--list-unused-tags',
            required=False,
            action='store_true',
            help='''List unused tags.''')

        parser.add(
            '--delete-unused-tags',
            required=False,
            action='store_true',
            help='''Delete unused tags.''')

        parser.add(
            '--task-type',
            required=False,
            default='all',
            type=str,
            choices=['habits', 'dailies', 'todos', 'rewards', 'all'],
            help='Specify the task type to operate on')

        parser.add(
            '--show-uuid',
            required=False,
            action='store_true',
            help='''Show the task UUID. Useful for finding spell targets.''')

        self.print_help = parser.print_help
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

        # Convert the task type option to the HabiticaTaskTypes enum
        if self._config.task_type == 'all':
            # None is used in the HabiticaService API to indicate all tasks
            self.task_type = None
            self.task_type_name = 'tasks'
        else:
            self.task_type = sb.HabiticaTaskTypes.__members__[
                self._config.task_type]
            self.task_type_name = self.task_type.value

        if self._config.list_tasks:
            self.list_tasks()
        elif self._config.delete_tasks:
            self.delete_tasks()
        elif self._config.list_tags:
            self.list_tags()
        elif self._config.list_unused_tags:
            self.list_unused_tags()
        elif self._config.delete_unused_tags:
            if self._config.dry_run:
                logging.getLogger(__name__).debug(
                    "Dry run, falling back to listing unused tags")
                self.list_unused_tags()
            else:
                self.delete_unused_tags()
        else:
            print()
            self.print_help()

        # return False if finished, and True to be updated again.
        return False

    def delete_tasks(self):
        """Deletes all user tasks"""
        logging.getLogger(__name__).debug(
            'Deleting all %s', self.task_type_name)

        tasks = self._hs.get_tasks(task_type=self.task_type)
        for t in tasks:
            print('Deleting {0}'.format(t['text']))
            if not self.dry_run:
                self._hs.delete_task(t)
                sleep(1)

    def list_tasks(self):
        """Dumps all tasks"""
        print('*** Listing {0} ***'.format(self.task_type_name))
        print()

        tasks = self._hs.get_tasks(task_type=self.task_type)
        for t in tasks:
            if self._config.verbose:
                pprint(t)
            elif self._config.show_uuid:
                print('{0} ({1})'.format(t['text'], t['id']))
            else:
                print(t['text'])

    def list_tags(self):
        """Lists all tags"""
        print('*** Listing tags ***')
        print()
        self.__print_tags(self._hs.get_tags())

    def list_unused_tags(self):
        """Lists unused tags"""
        print('*** Listing unused tags ***')
        print()
        self.__print_tags(self.__get_unused_tags().values())

    def delete_unused_tags(self):
        """Deletes unused tags"""
        print('*** Deleting unused tags ***')
        print()
        self._hs.delete_tags(self.__get_unused_tags().values())

    def __get_unused_tags(self):
        """gets the dictionary of unused tags"""
        tags = self._hs.get_tags()
        tasks = self._hs.get_tasks()

        # simple m*n first implementation. No need to do something fancier
        # unless this is too slow

        # first, assume that all tags are unused
        unused_tags = {t['id']:t for t in tags}

        # Then, try to disprove that assumption by finding at least one task
        # that uses the tag
        for tag in tags:
            for task in tasks:
                if tag['id'] in task['tags']:
                    logging.getLogger(__name__).debug(
                        'tag %s is used', tag['name'])
                    del unused_tags[tag['id']]
                    break

        return unused_tags

    def __print_tags(self, tags):
        """ print the supplied list of tags.

        Args:
            tags (list): The tags to print
        """
        if not tags:
            print("No tags")
        else:
            for t in tags:
                if self._config.verbose:
                    pprint(t)
                else:
                    print(t['name'])
