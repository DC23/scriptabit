""" Poisoning and health regeneration plugin.
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

import scriptabit


class HealthEffects(scriptabit.IPlugin):
    """Official scriptabit plugin that implements a poisoning/health
    regeneration scenario based on player performance on dailies.
    """

    def __init__(self):
        """ Initialises the plugin. It is hard to do any significant work here
        as the yapsy framework instantiates plugins automatically. Thus extra
        arguments cannot be passed easily.
        """
        super().__init__()

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--he-max-hp-loss-per-day',
            required=False,
            default=20.0,
            type=float,
            help='Health Effects: Max amount of health loss per day')

        return parser

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """
        super().initialise(configuration, habitica_service)

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        This method will be ignored when single_shot returns True.
        The default interval is 60 minutes.

        Returns: float: The required update interval in minutes.
        """
        # For testing only. Actual use will be at 30 or 60 minutes
        return 0.02

    def update(self):
        """ Update the health effects plugin.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """
        super().update()
        return self._update_count < 3
