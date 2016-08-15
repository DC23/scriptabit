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

import pickle
from bidict import bidict, DuplicationBehavior


class TaskMap(object):
    """ Persistent 1-1 task mapping.
    """

    def __init__(self, filename=''):
        """ Initialise the TaskMap instance.

        Args:
            filename (str): The optional filename to load from.
        """
        super().__init__()
        if filename:
            with open(filename, 'rb') as f:
                self.__bidict = pickle.load(f)
        else:
            self.__bidict = bidict()

    def persist(self, filename):
        """ Persist the TaskMap instance to a file.

        Args:
            filename (str): The destination file name.

        """
        with open(filename, 'wb') as f:
            pickle.dump(self.__bidict, f, pickle.HIGHEST_PROTOCOL)

    def map(self, src, dst):
        """ Create a mapping between a source and destination task.

        Args:
            src (Task): The source task.
            dst (Task): The destination task.
        """
        self.__bidict.put(
            src.id,
            dst.id,
            on_dup_key=DuplicationBehavior.RAISE,
            on_dup_val=DuplicationBehavior.RAISE,
            on_dup_kv=DuplicationBehavior.RAISE)

    def get_dst_id(self, src):
        """ Get the mapped destination task ID for a source task.

        Args:
            src (Task): The source task.

        Returns:
            If a mapping exists, the destination task ID.

        returns:
            KeyError: if the input ID has no mapping.
        """
        return self.__bidict[src.id]

    def get_src_id(self, dst):
        """ Get the mapped source task ID for a destination task.

        Args:
            dst (Task): The destination task.

        Returns:
            If a mapping exists, the source task ID.

        returns:
            KeyError: if the input ID has no mapping.
        """
        return self.__bidict.inv[dst.id]

    def try_get_dst_id(self, src):
        """ Get the mapped destination task ID for a source task.

        Args:
            src (Task): The source task.

        Returns:
            If a mapping exists, the destination task ID, otherwise False.
        """
        return self.__bidict.get(src.id, False)

    def try_get_src_id(self, dst):
        """ Get the mapped source task ID for a destination task.

        Args:
            dst (Task): The destination task.

        Returns:
            If a mapping exists, the source task ID, otherwise False.
        """
        return self.__bidict.inv.get(dst.id, False)
