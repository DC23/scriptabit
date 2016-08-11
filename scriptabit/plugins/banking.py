""" Banking plugin.
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


class Banking(scriptabit.IPlugin):
    """scriptabit plugin that implements a banking feature. Allows deposits and
    withdrawals from a custom bank.
    """

    def __init__(self):
        """ Initialises the bank.
        """
        super().__init__()

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--bank-deposit',
            required=False,
            default=0,
            type=float,
            help='Banking: Deposit gold')

        parser.add(
            '--bank-withdraw',
            required=False,
            default=0,
            type=float,
            help='Banking: Withdraw gold')

        return parser

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """
        super().initialise(configuration, habitica_service)

    def update(self):
        """ Update the banking plugin.

        Returns: bool: False
        """
        super().update()

        # Do the banking thing
        if self.config.bank_deposit > 0:
            logging.getLogger(__name__).info(
                'Deposit %d',
                self.config.bank_deposit)

        if self.config.bank_withdraw > 0:
            logging.getLogger(__name__).info(
                'Withdraw %d',
                self.config.bank_withdraw)

        return False
