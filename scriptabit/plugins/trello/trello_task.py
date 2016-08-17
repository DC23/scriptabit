# -*- coding: utf-8 -*-
""" Implements a Trello synchronisation task.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
from datetime import datetime
import pytz

from scriptabit import CharacterAttribute, Difficulty, Task


class TrelloTask(Task):
    """ Defines a Trello synchronisation task.
    """

    def __init__(self, card, force_completed=False):
        """ Initialise the task.

        Args:
            card (Trello.Card): The underlying Trello card.
            force_completed (bool): If True, the task will report as completed
                even if card.closed is False.
        """
        super().__init__()
        self.__card = card
        self.__force_completed = force_completed

    @property
    def id(self):
        """ Task id """
        return self.__card.id

    @property
    def name(self):
        """ Task name """
        return self.__card.name

    @name.setter
    def name(self, name):
        """ Task name """
        self.__card.set_name(name)

    @property
    def description(self):
        """ Task description """
        return self.__card.description

    @description.setter
    def description(self, description):
        """ Task description """
        self.__card.set_description(description)

    @property
    def completed(self):
        """ Task completed """
        return self.__force_completed or self.__card.closed

    @completed.setter
    def completed(self, completed):
        """ Task completed """
        self.__card.set_closed(completed)

    @property
    def difficulty(self):
        """ Task difficulty """
        card_labels = [x.name for x in self.__card.labels]
        if card_labels:
            for dl in Difficulty:
                if dl.name in card_labels:
                    return dl
        return Difficulty.easy

    @difficulty.setter
    def difficulty(self, difficulty):
        """ Task difficulty """
        if not isinstance(difficulty, Difficulty):
            raise TypeError
        raise NotImplementedError
        # TODO: apply a label to set the difficulty

    @property
    def attribute(self):
        """ Task character attribute """
        card_labels = [x.name for x in self.__card.labels]
        if card_labels:
            for al in CharacterAttribute:
                if al.name in card_labels:
                    return al
        return CharacterAttribute.strength

    @attribute.setter
    def attribute(self, attribute):
        """ Task character attribute """
        if not isinstance(attribute, CharacterAttribute):
            raise TypeError
        raise NotImplementedError
        # TODO: apply a label to set the attribute

    @property
    def due_date(self):
        """ The due date if there is one, or None. """
        due = self.__card.due_date
        if due:
            return due.astimezone(tz=pytz.utc)
        return None

    @due_date.setter
    def due_date(self, due_date):
        """ Sets or clears the due date. """
        if due_date and not isinstance(due_date, datetime):
            raise TypeError
        raise NotImplementedError
