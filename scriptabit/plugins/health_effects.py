""" Poisoning and health regeneration plugin.
"""

import logging

from scriptabit.plugin_interfaces import IOfficialPlugin


class HealthEffects(IOfficialPlugin):
    """Official scriptabit plugin that implements a poisoning/health
    regeneration scenario based on player performance on dailies.
    """

    def __init__(self):
        """ Initialises the plugin. It is hard to do any significant work here
        as the yapsy framework instantiates plugins automatically. Thus extra
        arguments cannot be passed easily.
        """

        super().__init__()

    def initialise(self, configuration, habitica_service):
        """ Initialises the plugin.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
        """

        super(IOfficialPlugin).initialise(configuration, habitica_service)

    def single_shot(self):
        """ Indicates whether this plugin should be executed just once, or
        from the update loop.

        Returns: bool: True if the plugin executes just once; otherwise False.
        """

        return False

    def update_interval_minutes(self):
        """ Indicates the required update interval in integer minutes.

        This method will be ignored when single_shot returns True.
        The default interval is 60 minutes.

        Returns: int: The required update interval in minutes.
        """

        # For testing only. Actual use will be at 30 or 60 minutes
        return 1

    def update(self):
        """ For updateable plugins (single_shot() == False), this update method
        will be called once on every update cycle, with the frequency determined
        by the value returned from update_interval_minutes().

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """

        super(IOfficialPlugin).update()
        self.__update_count += 1
        logging.getLogger(__name__).debug(
            'HealthEffects update %d',
            self.__update_count)
        return self.__update_count >= 5
