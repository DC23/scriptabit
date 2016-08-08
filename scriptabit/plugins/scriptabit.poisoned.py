""" Poisoning and health regeneration scenario.
"""

from yapsy.IPlugin import IPlugin


class Poisoned(IPlugin):

    def activate():
        logging.getLogger(__name__).debug('Poisoning activated')

    def deactivate():
        logging.getLogger(__name__).debug('Poisoning deactivated')
