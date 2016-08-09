""" Poisoning and health regeneration scenario.
"""

from scriptabit.plugin_interfaces import IOfficialPlugin


class Poisoned(IOfficialPlugin):
    """Official scriptabit plugin that implements a poisoning/health
    regeneration scenario based on player performance on dailies.
    """

    def id(self):
        """Returns the plugin ID.

        The ID is used to select the plugin through the command line interface,
        and therefore unambiguous strings without spaces are preferred.
        """

        return "sbpoisoned"

