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

from bidict import bidict


class TaskMapping(object):
    """ Persistent 1-1 task mapping.
    """

    def __init__(self):
        """ Initialise the TaskMapping instance """
        super().__init__()

    @staticmethod
    def create(filename):
        """ Factory method to create a TaskMapping instance.

        Args:
            filename (str): The filename to load from.
        """
        raise NotImplemented

    def persist(self, filename):
        """ Persist the TaskMapping instance to a file.

        Args:
            filename (str): The destination file name.

        """
        raise NotImplemented

    def map(self, src, dst):
        """ Create a mapping between a source and destination task.

        Args:
            src (Task): The source task.
            dst (Task): The destination task.

        """
        raise NotImplemented

    def get_dst_id(self, src):
        """ Get the mapped destination task ID for a source task.

        Args:
            src (Task): The source task.

        Returns:
            If a mapping exists, the destination task ID, otherwise False.
        """
        raise NotImplemented

    def get_src_id(self, dst):
        """ Get the mapped source task ID for a destination task.

        Args:
            dst (Task): The destination task.

        Returns:
            If a mapping exists, the source task ID, otherwise False.
        """
        raise NotImplemented
