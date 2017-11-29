# -*- coding: utf-8 -*-
""" Defines persistent 1-1 task mappings.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *

import sys
import json
from bidict import bidict, DuplicationPolicy


class TaskMap(object):
    """ Persistent 1-1 task mapping.
    """
    def __init__(self, filename=None):
        """ Initialise the TaskMap instance.

        Args:
            filename (str): The optional filename to load from.
        """
        super().__init__()

        # try to load from the file, defaulting to empty bidict if the load
        # fails for any reason
        try:
            self.__bidict = bidict()
            with open(filename, 'r') as f:
                self.__bidict = bidict(json.load(f))
        except:
            self.__bidict = bidict()

    def __map(self, a, b):
        """ Associate two ID strings """
        self.__bidict.put(
            a,
            b,
            on_dup_key=DuplicationPolicy.RAISE,
            on_dup_val=DuplicationPolicy.RAISE,
            on_dup_kv=DuplicationPolicy.RAISE)

    def persist(self, filename):
        """ Persist the TaskMap instance to a file.

        Args:
            filename (str): The destination file name.
        """
        with open(filename, 'w') as f:
            if sys.version_info < (3, 0):
                x = json.dumps(dict(self.__bidict),
                               encoding='UTF-8',
                               ensure_ascii=False)
            else:
                x = json.dumps(dict(self.__bidict),
                               ensure_ascii=False)

            f.write(x)

    def map(self, src, dst):
        """ Create a mapping between a source and destination task.

        Args:
            src (Task): The source task.
            dst (Task): The destination task.
        """
        self.__map(src.id, dst.id)

    def unmap(self, src_id):
        """ Delete a mapping.

        Args:
            src_id: The source id to unmap.
        """
        self.__bidict.pop(src_id)

    def get_dst_id(self, _id):
        """ Get the mapped destination task ID for a source task.

        Args:
            _id: The source task ID.

        Returns:
            If a mapping exists, the destination task ID.

        Raises:
            KeyError: if the input ID has no mapping.
        """
        return self.__bidict[_id]

    def get_src_id(self, _id):
        """ Get the mapped source task ID for a destination task.

        Args:
            _id: The destination task.

        Returns:
            If a mapping exists, the source task ID.

        Raises:
            KeyError: if the input ID has no mapping.
        """
        return self.__bidict.inv[_id]

    def try_get_dst_id(self, _id):
        """ Get the mapped destination task ID for a source task.

        Args:
            _id: The source task ID

        Returns:
            str: If a mapping exists, the destination task ID, otherwise False.
        """
        return self.__bidict.get(_id, False)

    def try_get_src_id(self, _id):
        """ Get the mapped source task ID for a destination task.

        Args:
            _id: The destination task ID

        Returns:
            str: If a mapping exists, the source task ID, otherwise False.
        """
        return self.__bidict.inv.get(_id, False)

    def get_all_src_keys(self):
        """ Gets a list of all source keys.

        Returns:
            list: all source keys.
        """
        return self.__bidict.keys()

    def get_all_dst_keys(self):
        """ Gets a list of all destination keys.

        Returns:
            list: all destination keys.
        """
        return self.__bidict.inv.keys()
