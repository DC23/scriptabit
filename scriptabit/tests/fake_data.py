# -*- coding: utf-8 -*-
""" Functions for generating fake JSON data """

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
from builtins import *
import json

from scriptabit import HabiticaTask


def get_fake_stats(
    _id='this is not a common guid',
    con=10,
    _int=11,
    per=12,
    _str=13,
    gp=194.4,
    hp=47.21,
    lvl=4,
    exp=34,
    toNextLevel=180,
    mp=42,
    maxMP=55):
    """ Generates some fake stats data in dictionary and json form, for testing
    with requests_mock. """

    stats = \
    {
        'con':con,
        'int':_int,
        'per':per,
        'str':_str,
        'gp':gp,
        'hp':hp,
        'lvl':lvl,
        'exp':exp,
        'toNextLevel':toNextLevel,
        'mp':mp,
        'maxMP':maxMP,
    }

    _json = json.dumps(
        {
            'data':
            {
                'id':_id,
                'stats': stats,
            }
        })

    return (stats, _json)

def get_fake_task(
    _id='',
    alias='',
    attribute='str',
    notes='notes',
    text='text',
    _type='habit',
    completed=False,
    value=0):
    """Generates test task data as both a dictionary and json"""

    task = \
    {
        '_id': _id,
        'alias': alias,
        'attribute': attribute,
        'notes': notes,
        'priority': 1,
        'text': text,
        'type': _type,
        'value': value,
        'completed': completed,
    }

    _json = json.dumps({'data': task})

    return (task, _json)
