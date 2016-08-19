"""Scriptabit plugin that implements a banking feature. Allows deposits and
withdrawals from a custom bank.

If neither a deposit or withdrawal is specified, then the balance is
reported but not changed.

Deposits and withdrawals are capped to the amount available, so a simple
way to deposit or withdraw all the gold is to specify an amount larger than
the balance.
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
    """ Implements the banking plugin.
    """
    def __init__(self):
        """ Initialises the Banking instance. """
        super().__init__()
        self.__bank = None
        self.__bank_balance = 0
        self.__user_balance = 0

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the banking plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        super().initialise(configuration, habitica_service, data_dir)

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

    @staticmethod
    def get_balance_string(amount):
        """Gets the formatted bank balance string for a given amount"""
        return 'Balance: {0}'.format(amount)

    @staticmethod
    def get_balance_from_string(s):
        """Gets the bank balance from the formatted string"""
        matches = re.findall(r'\d+', s)
        if matches:
            return int(matches[0])
        return 0

    def update(self):
        """ Update the banking plugin.

        Returns: bool: False
        """
        super().update()

        # Get or create the banking task
        self.__bank = self._hs.get_task(alias='scriptabit_banking')
        if not self.__bank:
            logging.getLogger(__name__).info('Creating new bank task')
            self.__bank = self._hs.create_task({
                'alias': 'scriptabit_banking',
                'attribute': 'per',
                'priority': 1,
                'text': self._config.bank_name,
                'type': 'reward',
                'value': 0})

        # Get the user and bank balances
        self.__bank_balance = Banking.get_balance_from_string(
            self.__bank['notes'])
        self.__user_balance = self._hs.get_stats()['gp']

        logging.getLogger(__name__).info(
            'Bank balance: %f',
            self.__bank_balance)
        logging.getLogger(__name__).info(
            'User balance: %f',
            self.__user_balance)

        # Do the banking thing
        if self._config.bank_deposit > 0:
            self.__deposit()
        elif self._config.bank_withdraw > 0:
            self.__withdraw()

        return False

    def __deposit(self):
        """ Deposit money to the bank.
        """
        # Don't deposit more money than the user has
        amount = min(
            math.trunc(self.__user_balance),
            self._config.bank_deposit)
        logging.getLogger(__name__).info('Deposit: %d', amount)

        # update the bank balance
        self.__bank['notes'] = Banking.get_balance_string(
            self.__bank_balance + amount)
        self._hs.upsert_task(self.__bank)

        # subtract the gold from user balance
        self._hs.set_gp(max(0, self.__user_balance - amount))

        self.__notify('Deposited: {0}'.format(amount))

    def __withdraw(self):
        """ Withdraw money from the bank.
        """
        # Don't withdraw more money than the bank has
        amount = min(self.__bank_balance, self._config.bank_withdraw)
        logging.getLogger(__name__).info('Withdraw: %d', amount)

        # update the bank balance
        new_balance = max(0, self.__bank_balance - amount)
        self.__bank['notes'] = Banking.get_balance_string(new_balance)
        self._hs.upsert_task(self.__bank)

        # add the gold to user balance
        self._hs.set_gp(self.__user_balance + amount)

        self.__notify('Withdrew: {0}'.format(amount))

    def __notify(self, message):
        """ Notify the Habitica user """
        logging.getLogger(__name__).info(message)
        scriptabit.UtilityFunctions.upsert_notification(
            self._hs,
            alias='scriptabit_banking_notify',
            text=':moneybag: ' + message)
