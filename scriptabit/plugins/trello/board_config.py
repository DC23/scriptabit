# -*- coding: utf-8 -*-
""" Trello board configuration
"""

# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging

from scriptabit import CharacterAttribute, Difficulty


class BoardConfig(object):
    """ Board configuration details, parsed from the command line arguments.

    Attributes:
        name (str): the board name.
        all_cards (bool): If True, all cards should be used; otherwise only
            cards assigned to the current user should be used.
        difficulty (scriptabit.Difficulty): the default difficulty for this
            board.
        attribute (scriptabit.CharacterAttribute): The default character
            attribute for this board.
    """
    def __init__(self, board_config_string, delimiter='|'):
        """ Initialises the BoardConfig instance.

        Args:
            board_config_string (str): The board configuration string. This
                is a packed string containing up to four options, delimited
                by `delimiter`. E.G.::

                    'board_name|difficulty|attribute|user'

                If the user field is not specified, then it defaults to
                `all_cards` = True. Specifying any characters for the fourth
                user field will set all_cards to False.

            delimiter (str): The delimiter character to use.
        """
        values = board_config_string.split(delimiter)
        count = len(values)
        if not values[0]:
            raise ValueError('board_config_string')

        self.name = values[0]
        self.all_cards = False if count > 3 else True
        self.difficulty = Difficulty.default
        self.attribute = CharacterAttribute.default
