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
            '--bank-max-fee',
            required=False,
            type=int,
            default=100,
            help='''Banking: The maximum fee limit. Set to 0 to disable fees.
Values up to 600 will make transactions very expensive, while going beyond
600 will start to make small transactions cost more than the transaction
amount.''')

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
            tag = self._hs.create_tags(['scriptabit'])
            self.__bank = self._hs.create_task({
                'alias': 'scriptabit_banking',
                'attribute': 'per',
                'priority': 1,
                'text': self._config.bank_name,
                'type': 'reward',
                'tags': [tag[0]['id']],
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
            self.deposit()
        elif self._config.bank_withdraw > 0:
            self.withdraw()
        elif self._config.bank_tax > 0:
            self.pay_tax()

        return False

    def pay_tax(self):
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
            self.update_bank_balance(new_balance)
            total_paid += bank_amount

        message = ':smiling_imp: Taxes paid: {0}'.format(total_paid)
        self.notify(message)

    def deposit(self):
        """ Deposit money to the bank.
        """
        # Don't deposit more money than the user has
        gross_amount = min(
            math.trunc(self.__user_balance),
            self._config.bank_deposit)
        fee = math.trunc(self.calculate_fee(gross_amount))
        nett_amount = max(0, gross_amount - fee)

        # update the bank balance
        self.update_bank_balance(self.__bank_balance + nett_amount)

        # subtract the gold from user balance
        self._hs.set_gp(max(0, self.__user_balance - gross_amount))

        message = 'Deposit: {0}, Fee: {1}'.format(nett_amount, fee)
        self.notify(message)

    def withdraw(self):
        """ Withdraw money from the bank.
        """
        # Don't withdraw more money than the bank has
        gross_amount = min(self.__bank_balance, self._config.bank_withdraw)
        fee = math.trunc(self.calculate_fee(gross_amount))
        nett_amount = max(0, gross_amount - fee)

        # update the bank balance
        new_balance = max(0, self.__bank_balance - gross_amount)
        self.update_bank_balance(new_balance)

        # add the gold to user balance
        self._hs.set_gp(self.__user_balance + nett_amount)

        message = 'Withdrew: {0}, Fee: {1}'.format(nett_amount, fee)
        self.notify(message)

    def notify(self, message):
        """ Notify the Habitica user """
        logging.getLogger(__name__).info(message)
        scriptabit.UtilityFunctions.upsert_notification(
            self._hs,
            text=':moneybag: ' + message)

    def update_bank_balance(self, new_balance):
        """ Updates the bank balance.

        Args:
            new_balance (float): The new balance.
        """
        new_balance = math.trunc(new_balance)
        self.__bank['notes'] = Banking.get_balance_string(new_balance)
        self.__bank['value'] = new_balance
        self._hs.upsert_task(self.__bank)

    def calculate_fee(self, amount):
        """ Calculates the fee for a given transaction amount.

        Args:
            amount (float): The transaction amount.

        Returns:
            float: the transaction fee.
        """
        # Diminishing returns exponential function, tuned to be expensive at
        # amounts < 1000 gold, but to flatten quickly for amounts > 1000
        limit = max(0, self._config.bank_max_fee)
        return limit * (1 - math.exp(-0.0015 * amount))
