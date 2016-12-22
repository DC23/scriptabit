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
        self.__bank_traits = None
        self.print_help = None

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the banking plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        super().initialise(configuration, habitica_service, data_dir)

    @staticmethod
    def supports_dry_runs():
        """ The Banking plugin supports dry runs.

        Returns:
            bool: True
        """
        return True

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.
        """
        parser = super().get_arg_parser()

        parser.add(
            '-d',
            '--bank-deposit',
            required=False,
            default=0,
            type=int,
            help='Banking: Deposit to the bank')

        parser.add(
            '-w',
            '--bank-withdraw',
            required=False,
            default=0,
            type=int,
            help='Banking: Withdraw from the bank')

        parser.add(
            '-b',
            '--bank-balance',
            required=False,
            action='store_true',
            help='Banking: Display balance')

        parser.add(
            '--bank-tax',
            required=False,
            default=0,
            type=int,
            help='''Banking: Pay your taxes. Only applies to the gold bank.
Deducts the specified gold amount. If there is not enough gold in your main
balance, it tries the bank.''')

        parser.add(
            '--bank-max-fee',
            required=False,
            type=int,
            default=100,
            help='''Banking: The maximum fee limit. Set to 0 to disable fees.
Values up to 600 will make transactions very expensive, while going beyond
600 will start to make small transactions cost more than the transaction
amount.''')

        parser.add(
            '-bt',
            '--bank-type',
            required=False,
            default='gold',
            type=str,
            choices=['gold', 'mana', 'health'],
            help='Banking: select the type of bank.')

        self.print_help = parser.print_help
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

        stats = self._hs.get_stats()

        # determine the bank type and set the traits object
        if self._config.bank_type == 'mana':
            self.__bank_traits = {
                'alias': 'scriptabit_mana_bank',
                'name': ':blue_heart: Mana Bank',
                'stat': 'mp',
                'allow_tax': False,
                'icon': ':blue_heart:',
                'min_user_balance': 0,
                'max_user_balance': stats['maxMP'],
            }
        elif self._config.bank_type == 'health':
            self.__bank_traits = {
                'alias': 'scriptabit_health_bank',
                'name': ':heart: Health Bank',
                'stat': 'hp',
                'allow_tax': False,
                'icon': ':heart:',
                'min_user_balance': 1,
                'max_user_balance': stats['maxHealth'],
            }
        else:
            # assume gold
            self.__bank_traits = {
                'alias': 'scriptabit_banking',
                'name': ':moneybag: Gold Bank',
                'stat': 'gp',
                'allow_tax': True,
                'icon': ':moneybag:',
                'min_user_balance': 0,
                'max_user_balance': False,
            }

        # Get or create the banking task
        self.__bank = self._hs.get_task(self.__bank_traits['alias'])
        if not self.__bank:
            logging.getLogger(__name__).info('Creating new bank task')
            tag = self._hs.create_tags(['scriptabit'])
            self.__bank = self._hs.create_task({
                'alias': self.__bank_traits['alias'],
                'attribute': 'per',
                'priority': 1,
                'text': self.__bank_traits['name'],
                'type': 'reward',
                'tags': [tag[0]['id']],
                'value': 0})

        # Get the user and bank balances
        self.__bank_balance = Banking.get_balance_from_string(
            self.__bank['notes'])
        self.__user_balance = stats[self.__bank_traits['stat']]

        # Do the banking thing
        if self._config.bank_deposit > 0:
            self.deposit()
        elif self._config.bank_withdraw > 0:
            self.withdraw()
        elif self._config.bank_tax > 0:
            self.pay_tax()
        elif self._config.bank_balance:
            logging.getLogger(__name__).info(
                'Bank balance: %f',
                self.__bank_balance)
            logging.getLogger(__name__).info(
                'User balance: %f',
                self.__user_balance)
        else:
            print()
            self.print_help()

        return False

    def pay_tax(self):
        """ Pays taxes, trying first from the main balance, and then from the
        bank.
        """
        if not self.__bank_traits['allow_tax']:
            return

        tax = self._config.bank_tax

        # subtract from user balance
        user_amount = min(self.__user_balance, tax)
        if not self.dry_run:
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
            math.trunc(self.__user_balance - self.__bank_traits['min_user_balance']),
            self._config.bank_deposit)
        fee = math.trunc(self.calculate_fee(gross_amount))
        nett_amount = max(0, gross_amount - fee)

        # update the bank balance
        self.update_bank_balance(self.__bank_balance + nett_amount)

        # subtract from user balance
        if not self.dry_run:
            if self._config.bank_type == 'mana':
                self._hs.set_mp(max(0, self.__user_balance - gross_amount))
            elif self._config.bank_type == 'health':
                self._hs.set_hp(max(0, self.__user_balance - gross_amount))
            else:
                self._hs.set_gp(max(0, self.__user_balance - gross_amount))

        message = '{2} Deposit: {0}, Fee: {1}'.format(
            nett_amount,
            fee,
            self.__bank_traits['icon'])
        self.notify(message)

    def withdraw(self):
        """ Withdraw money from the bank.
        """
        # Don't withdraw more money than the bank has
        gross_amount = min(self.__bank_balance, self._config.bank_withdraw)

        # If the traits supports a max user balance, don't withdraw more
        # than that amount
        if self.__bank_traits['max_user_balance']:
            gross_amount = min(
                max(0, self.__bank_traits['max_user_balance'] - self.__user_balance),
                gross_amount)
            print('capping withdrawal to ', gross_amount)

        fee = math.trunc(self.calculate_fee(gross_amount))
        nett_amount = max(0, gross_amount - fee)

        # update the bank balance
        new_balance = max(0, self.__bank_balance - gross_amount)
        self.update_bank_balance(new_balance)

        # add to user balance
        if not self.dry_run:
            if self._config.bank_type == 'mana':
                self._hs.set_mp(self.__user_balance + nett_amount)
            elif self._config.bank_type == 'health':
                self._hs.set_hp(self.__user_balance + nett_amount)
            else:
                self._hs.set_gp(self.__user_balance + nett_amount)

        message = '{2} Withdrew: {0}, Fee: {1}'.format(
            nett_amount,
            fee,
            self.__bank_traits['icon'])
        self.notify(message)

    def update_bank_balance(self, new_balance):
        """ Updates the bank balance.

        Args:
            new_balance (float): The new balance.
        """
        new_balance = math.trunc(new_balance)
        self.__bank['notes'] = Banking.get_balance_string(new_balance)
        self.__bank['value'] = new_balance
        if not self.dry_run:
            self._hs.upsert_task(self.__bank)

    def calculate_fee(self, amount):
        """ Calculates the fee for a given transaction amount.

        Args:
            amount (float): The transaction amount.

        Returns:
            float: the transaction fee.
        """
        if self._config.bank_type == 'mana':
            return 20 * (1 - math.exp(-0.01 * amount))
        elif self._config.bank_type == 'health':
            return 5 * (1 - math.exp(-0.07 * amount))
        else:
            # Diminishing returns exponential function, tuned to be expensive at
            # amounts < 1000 gold, but to flatten quickly for amounts > 1000
            limit = max(0, self._config.bank_max_fee)
            return limit * (1 - math.exp(-0.0015 * amount))
