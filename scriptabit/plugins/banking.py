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
        self.__transaction_fee = 0

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
            '--bank-tax',
            required=False,
            default=0,
            type=int,
            help='''Banking: Pay your taxes. Deducts the specified gold amount.
If there is not enough gold in your main balance, it tries the bank.''')

        parser.add(
            '--bank-name',
            required=False,
            default=':moneybag: The Scriptabit Bank',
            type=str,
            help='Banking: Sets the bank name.')

        parser.add(
            '--bank-fee-percentage',
            required=False,
            default=0.02,
            type=float,
            help='''Banking: Bank fee percentage. This percentage is deducted
from each transaction''')

        return parser

    @staticmethod
    def get_balance_string(amount):
        """Gets the formatted bank balance string for a given amount"""
        return 'Balance: {0}'.format(math.trunc(amount))

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

        fee_rate = min(max(0, self._config.bank_fee_percentage), 1)

        logging.getLogger(__name__).info(
            'Bank balance: %f',
            self.__bank_balance)
        logging.getLogger(__name__).info(
            'User balance: %f',
            self.__user_balance)
        logging.getLogger(__name__).info(
            'Transaction fee percentage: %f',
            fee_rate)

        # Do the banking thing
        if self._config.bank_deposit > 0:
            self.__deposit(fee_rate)
        elif self._config.bank_withdraw > 0:
            self.__withdraw(fee_rate)
        elif self._config.bank_tax > 0:
            self.__pay_tax()

        return False

    def __pay_tax(self):
        """ Pays taxes, trying first from the main balance, and then from the
        bank.
        """
        tax = self._config.bank_tax

        # subtract from user balance
        user_amount = min(self.__user_balance, tax)
        self._hs.set_gp(max(0, self.__user_balance - user_amount))
        total_paid = user_amount

        # tax still owing?
        tax -= user_amount
        if tax > 0:
            # deduct balance from bank if we can
            bank_amount = min(self.__bank_balance, tax)
            new_balance = max(0, self.__bank_balance - bank_amount)
            self.__bank['notes'] = Banking.get_balance_string(new_balance)
            self._hs.upsert_task(self.__bank)
            total_paid += bank_amount

        message = ':smiling_imp: Taxes paid: {0}'.format(total_paid)
        self.__notify(message)

    def __deposit(self, fee_rate):
        """ Deposit money to the bank.

        Args:
            fee_rate (float): The percentage transaction fee
        """
        # Don't deposit more money than the user has
        gross_amount = min(
            math.trunc(self.__user_balance),
            self._config.bank_deposit)
        fee = math.trunc(gross_amount * fee_rate)
        nett_amount = gross_amount - fee

        # update the bank balance
        self.__bank['notes'] = Banking.get_balance_string(
            self.__bank_balance + nett_amount)
        self._hs.upsert_task(self.__bank)

        # subtract the gold from user balance
        self._hs.set_gp(max(0, self.__user_balance - gross_amount))

        message = 'Deposit: {0}, Transaction fee: {1}'.format(nett_amount, fee)
        self.__notify(message)

    def __withdraw(self, fee_rate):
        """ Withdraw money from the bank.

        Args:
            fee_rate (float): The percentage transaction fee
        """
        # Don't withdraw more money than the bank has
        gross_amount = min(self.__bank_balance, self._config.bank_withdraw)
        fee = math.trunc(gross_amount * fee_rate)
        nett_amount = gross_amount - fee

        # update the bank balance
        new_balance = max(0, self.__bank_balance - gross_amount)
        self.__bank['notes'] = Banking.get_balance_string(new_balance)
        self._hs.upsert_task(self.__bank)

        # add the gold to user balance
        self._hs.set_gp(self.__user_balance + nett_amount)

        message = 'Withdrew: {0}, Transaction fee: {1}'.format(nett_amount, fee)
        self.__notify(message)

    def __notify(self, message):
        """ Notify the Habitica user """
        logging.getLogger(__name__).info(message)
        scriptabit.UtilityFunctions.upsert_notification(
            self._hs,
            text=':moneybag: ' + message)
