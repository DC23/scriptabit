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
import math
import re

import scriptabit


class Banking(scriptabit.IPlugin):
    """scriptabit plugin that implements a banking feature. Allows deposits and
    withdrawals from a custom bank.

    If neither a deposit or withdrawal is specified, then the balance is
    reported but not changed.
    """

    def initialise(self, configuration, habitica_service):
        """ Initialises the banking plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """
        super().initialise(configuration, habitica_service)
        # self.__uf = scriptabit.UtilityFunctions(configuration, habitica_service)

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--bank-deposit',
            required=False,
            default=0,
            type=int,
            help='Banking: Deposit gold')

        parser.add(
            '--bank-withdraw',
            required=False,
            default=0,
            type=int,
            help='Banking: Withdraw gold')

        parser.add(
            '--bank-name',
            required=False,
            default=':moneybag: The Scriptabit Bank',
            type=str,
            help='Banking: Sets the bank name.')

        return parser

    @classmethod
    def get_balance_string(amount):
        """Gets the formatted bank balance string for a given amount"""
        return 'Balance: {0}'.format(amount)

    @classmethod
    def get_balance_from_string(s):
        """Gets the bank balance from the formatted string"""
        return int(re.findall('\d+', s)[0])

    def update(self):
        """ Update the banking plugin.

        Returns: bool: False
        """
        super().update()

        print()

        # Get the banking task
        default_bank = {
            'alias': 'scriptabit_banking',
            'attribute': 'per',
            'notes': Banking.get_balance_string(0),
            'priority': 1,
            'text': self._config.bank_name,
            'type': 'reward',
            'value': 0}
        bank = self._hs.upsert_task(default_bank)

        print(bank)

        # Get the user and bank balances
        bank_balance = Banking.get_balance_from_string(bank['notes'])
        user_balance = self._hs.get_stats()['gp'] # note this is a float!

        logging.getLogger(__name__).info(
            'Bank balance: {0}'.format(bank_balance))
        logging.getLogger(__name__).info(
            'User balance: {0}'.format(user_balance))

        # Do the banking thing
        if self._config.bank_deposit > 0:
            # Don't deposit more money than the user has
            amount = min(
                math.trunc(user_balance),
                self._config.bank_deposit)
            logging.getLogger(__name__).info('Depositing %d', amount)

            # update the bank balance
            bank['notes'] = Banking.get_balance_string(bank_balance + amount)
            self._hs.upsert_task(bank)

            # subtract the gold from user balance
            self._hs.set_gp(max(0, user_balance - amount))

            # avoid being able to do a deposit and withdrawal at once,
            # as this would introduce gold balance bugs
            return False

        if self._config.bank_withdraw > 0:
            # Don't withdraw more money than the bank has
            amount = min(bank_balance, self._config.bank_withdraw)
            logging.getLogger(__name__).info('Withdraw %d', amount)

            # update the bank balance
            new_balance = max(0, bank_balance - amount)
            bank['notes'] = Banking.get_balance_string(new_balance)
            self._hs.upsert_task(bank)

            # add the gold to user balance
            self._hs.set_gp(user_balance + amount)

            return False

        return False
