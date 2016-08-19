# -*- coding: utf-8 -*-
""" Unit tests for the trello plugin """
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *

import pytest
from scriptabit import Difficulty, CharacterAttribute
from .board_config import BoardConfig as BC

# 'board_name|difficulty|attribute|user'

def test_board_config_name_only():
    bc = BC('my board')
    assert bc.name == 'my board'
    assert bc.all_cards
    assert bc.difficulty == Difficulty.default
    assert bc.attribute == CharacterAttribute.default

def test_board_config_name_difficulty():
    bc = BC('my board|hard')
    assert bc.name == 'my board'
    assert bc.all_cards
    assert bc.difficulty == Difficulty.hard
    assert bc.attribute == CharacterAttribute.default

def test_board_config_name_attribute():
    bc = BC('my board||constitution')
    assert bc.name == 'my board'
    assert bc.all_cards
    assert bc.difficulty == Difficulty.default
    assert bc.attribute == CharacterAttribute.constitution

def test_board_config_name_user():
    bc = BC('my board|||user')
    assert bc.name == 'my board'
    assert not bc.all_cards
    assert bc.difficulty == Difficulty.default
    assert bc.attribute == CharacterAttribute.default

def test_board_config_name_difficulty_attribute():
    bc = BC('my board|trivial|intelligence')
    assert bc.name == 'my board'
    assert bc.all_cards
    assert bc.difficulty == Difficulty.trivial
    assert bc.attribute == CharacterAttribute.intelligence

def test_board_config_name_difficulty_attribute_user():
    bc = BC('my board|medium|perception|user')
    assert bc.name == 'my board'
    assert not bc.all_cards
    assert bc.difficulty == Difficulty.medium
    assert bc.attribute == CharacterAttribute.perception

def test_board_config_no_board_name():
    with pytest.raises(ValueError):
        bc = BC('|medium|perception|user')

def test_board_config_empty_string():
    with pytest.raises(ValueError):
        bc = BC('')

def test_board_config_invalid_difficulty():
    bc = BC('my board|bogus value')
    assert bc.difficulty == Difficulty.default

def test_board_config_invalid_attribute():
    bc = BC('my board||bogus value')
    assert bc.attribute == CharacterAttribute.default
