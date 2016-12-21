# -*- coding: utf-8 -*-
""" Spell casting
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
from time import sleep
import logging

import scriptabit

class Spellcast(scriptabit.IPlugin):
    """ Spellcast plugin implementation
    """
    def __init__(self):
        """ Initialises the plugin.
        Generally nothing to do here other than initialise any class attributes.
        """
        super().__init__()
        self.current_hp = None

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
            '--buff-target',
            required=False,
            default=None,
            type=str,
            help='buff target UUID')

        parser.add(
            '--cast-skill',
            required=False,
            default=None,
            type=str,
            help='cast a skill by API skill code')

        parser.add(
            '--preserve-user-hp',
            required=False,
            action='store_true',
            help='''Preserves the user HP at the pre-spell level.
This can be combined with Blessing to heal the party but not the user.''')

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
        skill = self._config.cast_skill
        target = self._config.buff_target
        count = self._config.max_updates or 1
        if skill and count:
            logging.getLogger(__name__).info(
                'Casting up to %d of %s', count, skill)

            self._store_hp()

            if not self._config.dry_run:
                for _ in range(count):
                    try:
                        result = self._hs.cast_skill_by_raw_spell_id(
                            skill,
                            target)
                        if not result['success']:
                            break
                        sleep(1)
                    except:
                        break

            self._restore_hp()

        # return False if finished, and True to be updated again.
        return False

    def _store_hp(self):
        'Store the current HP if required'
        if self._config.preserve_user_hp:
            self.current_hp = self._hs.get_stats()['hp']
            logging.getLogger(__name__).info(
                'Current HP: %f', self.current_hp)

    def _restore_hp(self):
        'Restore the current HP if required'
        if self._config.preserve_user_hp:
            logging.getLogger(__name__).info('Restoring HP: %f', self.current_hp)
            if not self._config.dry_run:
                self._hs.set_hp(self.current_hp)
