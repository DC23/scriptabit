# -*- coding: utf-8 -*-
""" Habitica pet care.

Options for batch hatching and feeding pets.
"""
# Ensure backwards compatibility with Python 2
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals)
from builtins import *
import logging
import random
from pprint import pprint
from time import sleep

import scriptabit


class PetCare(scriptabit.IPlugin):
    """ Habitica pet care
    """
    def __init__(self):
        """ Initialises the plugin.
        """
        super().__init__()
        self.__items = None
        self.__print_help = None
        self.__any_food = False

        # Generate the reference lists
        self.__base_pets = [
            'BearCub',
            'Cactus',
            'Dragon',
            'FlyingPig',
            'Fox',
            'LionCub',
            'PandaCub',
            'TigerCub',
            'Wolf',
        ]

        # TODO: other rare pets
        self.__rare_pets = [
            'Wolf-Veteran',
        ]

        # I don't need this list. Any pet that is not in the base pets,
        # special potions, or rare list is by default a quest pet
        # self.__quest_pets = [
            # 'Armadillo',
            # 'SeaTurtle',
            # 'Axolotl',
            # 'Treeling',
            # 'Falcon',
            # 'Snail',
            # 'Monkey',
            # 'Sabretooth',
            # 'Unicorn',
            # 'Snake',
            # 'Frog',
            # 'Horse',
            # 'Cheetah',
            # '',
            # '',
            # '',
            # '',
            # '',
            # '',
        # ]

        self.__preferred_foods = {
            'Base': ['Meat'],
            'CottonCandyBlue': ['CottonCandyBlue'],
            'CottonCandyPink': ['CottonCandyPink'],
            'Desert': ['Potatoe'],
            'Golden': ['Honey'],
            'Red': ['Strawberry'],
            'Skeleton': ['Fish'],
            'White': ['Milk'],
            'Zombie': ['RottenMeat'],
            'Shade': ['Chocolate'],
        }

        self.__base_potions = [
            'Base',
            'White',
            'Desert',
            'Red',
            'Shade',
            'Skeleton',
            'Zombie',
            'CottonCandyPink',
            'CottonCandyBlue',
            'Golden',
        ]

        self.__special_potions = [
            'Floral',
            'Thunderstorm',
            'Spooky',
            'Ghost',
        ]

        # augment the preferred foods with the special foods
        for potion in self.__base_potions:
            self.__preferred_foods[potion].append('Cake_{0}'.format(potion))
            self.__preferred_foods[potion].append('Candy_{0}'.format(potion))

        # build a list of all foods, for the special potions
        self.__all_foods = []
        for f in self.__preferred_foods.values():
            self.__all_foods.extend(f)

        for potion in self.__special_potions:
            self.__preferred_foods[potion] = self.__all_foods

    def get_arg_parser(self):
        """Gets the argument parser containing any CLI arguments for the plugin.

        Returns: argparse.ArgParser:  The `ArgParser` containing the argument
        definitions.
        """
        parser = super().get_arg_parser()

        parser.add(
            '--list-pets',
            required=False,
            action='store_true',
            help='Lists all pet-related items')

        parser.add(
            '--feed-pets',
            required=False,
            action='store_true',
            help='Batch pet feeding')

        parser.add(
            '--hatch-pets',
            required=False,
            action='store_true',
            help='Batch pet hatching')

        parser.add(
            '--any-pet-food',
            required=False,
            action='store_true',
            help='When feeding pets, allows the use of non-preferred food')

        parser.add(
            '--no-base-pets',
            required=False,
            action='store_true',
            help='Disables feeding of base pets')

        parser.add(
            '--quest-pets',
            required=False,
            action='store_true',
            help='Allows feeding of quest pets')

        parser.add(
            '--magic-pets',
            required=False,
            action='store_true',
            help='Allows feeding of magic pets')

        self.__print_help = parser.print_help

        return parser

    def initialise(self, configuration, habitica_service, data_dir):
        """ Initialises the plugin.

        Generally, any initialisation should be done here rather than in
        activate or __init__.

        Args:
            configuration (ArgParse.Namespace): The application configuration.
            habitica_service: the Habitica Service instance.
            data_dir (str): A writeable directory that the plugin can use for
                persistent data.
        """
        super().initialise(configuration, habitica_service, data_dir)
        logging.getLogger(__name__).info('Scriptabit Pet Care Services: looking'
                                         ' after your pets since yesterday')

        self.__items = self._hs.get_user()['items']
        self.__any_food = self._config.any_pet_food

    @staticmethod
    def supports_dry_runs():
        """ The PetCare plugin supports dry runs.

        Returns:
            bool: True
        """
        return True

    def update_interval_minutes(self):
        """ Indicates the required update interval in minutes.

        Returns: float: The required update interval in minutes.
        """
        return 30

    def update(self):
        """ This update method will be called once on every update cycle,
        with the frequency determined by the value returned from
        `update_interval_minutes()`.

        If a plugin implements a single-shot function, then update should
        return `False`.

        Returns: bool: True if further updates are required; False if the plugin
        is finished and the application should shut down.
        """

        # do work here
        if self._config.list_pets:
            self.list_pet_items(self.__items)
            return False

        if self._config.feed_pets:
            self.feed_pets()
            return False

        if self._config.hatch_pets:
            self.hatch_pets()
            return False

        # if no other options selected, print plugin specific help and exit
        self.__print_help()

        # return False if finished, and True to be updated again.
        return False

    def is_base_pet(self, pet, animal, potion):
        """ Is this a base pet?

        Args:
            pet (str): The full pet name.
            animal (str): The animal type.
            potion (str): The potion type.
        """
        return animal in self.__base_pets and potion in self.__base_potions

    def is_quest_pet(self, pet, animal, potion):
        """ Is this a quest pet?

        Args:
            pet (str): The full pet name.
            animal (str): The animal type.
            potion (str): The potion type.
        """
        return not (self.is_base_pet(pet, animal, potion)
                    or self.is_magic_pet(pet, animal, potion)
                    or self.is_rare_pet(pet, animal, potion))

    def is_magic_pet(self, pet, animal, potion):
        """ Is this a magic pet?

        Args:
            pet (str): The full pet name.
            animal (str): The animal type.
            potion (str): The potion type.
        """
        return potion in self.__special_potions

    def is_rare_pet(self, pet, animal, potion):
        """ Is this a rare pet?

        Args:
            pet (str): The full pet name.
            animal (str): The animal type.
            potion (str): The potion type.
        """
        return pet in self.__rare_pets

    def get_eggs(self, base=True, quest=False):
        """ Gets the filtered dictionary of available eggs. Values
        indicate current quantity.

        Args:
            base (bool): Includes or excludes standard eggs.
            eggs (bool): Includes or excludes quest eggs.

        Returns:
            dict: The dictionary of eggs and quantities.
        """
        eggs = {}

        for e, q in self.__items['eggs'].items():
            is_base_egg = e in self.__base_pets
            if base and is_base_egg:
                eggs[e] = q
            elif quest and not is_base_egg:
                eggs[e] = q

        return eggs

    def get_hatching_potions(self, base=True, magic=False):
        """ Gets the filtered dictionary of available hatching potions. Values
        indicate current quantity.

        Args:
            base (bool): Includes or excludes standard potions.
            magic (bool): Includes or excludes magic potions.

        Returns:
            dict: The dictionary of potions and quantities.
        """
        hp = {}

        for p, q in self.__items['hatchingPotions'].items():
            if (base and p in self.__base_potions) or\
                    (magic and p in self.__special_potions):
                hp[p] = q

        return hp

    def get_pets(
            self,
            base=True,
            magic=False,
            quest=False,
            rare=False,
            feedable_only=False):
        """ Gets a filtered list of current user pets.

        Args:
            base (bool): Includes or excludes base pets.
            magic (bool): Includes or excludes magic pets.
            quest (bool): Includes or excludes quest pets.
            rare (bool): Includes or excludes rare pets.
            feedable_only (bool): If true, only feedable pets are included.
                Pets where a matching mount exists are not feedable.

        Returns:
            list: the filtered pet list.
        """
        pets = []
        for pet, growth in self.__items['pets'].items():
            # Habitica indicates a pet that has been raised to a mount with
            # growth == -1. These pets are non-interactive, so exclude them.
            # There is no direct indication of the second pet (where a mount
            # also exists), so we check for the presence of a mount.
            if growth > 0:
                has_mount = self.__items['mounts'].get(pet, False)
                if not (feedable_only and has_mount):
                    animal, potion = pet.split('-')
                    if base and self.is_base_pet(pet, animal, potion):
                        pets.append(pet)
                    elif magic and self.is_magic_pet(pet, animal, potion):
                        pets.append(pet)
                    elif quest and self.is_quest_pet(pet, animal, potion):
                        pets.append(pet)
                    elif rare and self.is_rare_pet(pet, animal, potion):
                        pets.append(pet)

        return pets

    def feed_pets(self):
        """ Feeds all current pets. """
        pets = self.get_pets(
            base=not self._config.no_base_pets,
            magic=self._config.magic_pets,
            quest=self._config.quest_pets,
            rare=False,
            feedable_only=True)

        pet_count = 0
        food_count = 0
        mounts_raised = 0
        for pet in pets:
            if not self.has_any_food():
                logging.getLogger(__name__).info('Out of food')
                break
            try:
                food = self.get_food_for_pet(pet)
                fed_something = False
                while food:
                    fed_something = True
                    if self.dry_run:
                        response = {'data': -1, 'message': 'dry run'}
                    else:
                        response = self._hs.feed_pet(pet, food)

                    food_count += 1
                    self.consume_food(food)
                    growth = response['data']
                    logging.getLogger(__name__).info(
                        '%s (%d): %s', pet, growth, response['message'])

                    if growth > 0:
                        # growth > 0 indicates that the pet is still hungry
                        food = self.get_food_for_pet(pet)
                    else:
                        # growth <= 0 (-1 actually) indicates that the
                        # pet became a mount
                        mounts_raised += 1
                        break

                if fed_something and not self.dry_run:
                    sleep(2)  # sleep for a bit so we don't pound the server
            except Exception as e:
                logging.getLogger(__name__).warning(e)

            pet_count += 1

        message = \
            'Checked {1} pets, fed {0} pieces of food, raised {2} mounts'.\
            format(food_count, pet_count, mounts_raised)
        self.notify(message)

    def get_food_for_pet(self, pet):
        """ Gets a food item for a pet

        Args:
            pet (str): The composite pet name (animal-potion)

        Returns:
            str: The name of a suitable food if that food is in stock.
                If no suitable food is available, then None is returned.
        """
        # split the pet name
        _, potion = pet.split('-')

        if self.__any_food:
            for food, quantity in self.__items['food'].items():
                if quantity > 0:
                    return food
        else:
            for food in self.__preferred_foods[potion]:
                if self.has_food(food):
                    return food
        return None

    def has_any_food(self):
        """ Checks whether any food is left.

        Returns:
            bool: True if some food remains, otherwise False.
        """
        return sum(self.__items['food'].values()) > 0

    def has_food(self, food):
        """ Returns True if the food is in stock, otherwise False.

        Args:
            food (str): The food to check

        Returns:
            bool: True if the food is in stock, otherwise False.
        """
        return self.__items['food'].get(food, 0) > 0

    def consume_food(self, food):
        """ Consumes a food, updating the cached quantity.

        Args:
            food (str): The food.
        """
        quantity = self.__items['food'].get(food, 0)
        if quantity > 0:
            self.__items['food'][food] = quantity - 1

    @staticmethod
    def list_pet_items(items):
        """ Lists all pet-related inventory items.

        Args:
            items (dict): The Habitica user.items dictionary.
        """
        print()
        print('Food:')
        pprint(items['food'])
        print()
        print('Eggs:')
        pprint(items['eggs'])
        print()
        print('Hatching potions:')
        pprint(items['hatchingPotions'])
        print()
        print('Pets:')
        pprint(items['pets'])
        print()
        print('Mounts:')
        pprint(items['mounts'])

    def notify(self, message, **kwargs):
        """ Notify the Habitica user.

        If this is a dry run, then the message is logged. Otherwise the message
        is logged and posted to the Habitica notification panel.

        Args:
            message (str): The message.
            panel (bool): If True, the Habitica panel is updated.
        """
        emoticons = [
            'dog',
            'mouse',
            'snake',
            'snail',
            'monkey_face',
            'panda_face',
            'pig',
            'whale',
            'dragon',
            'monkey',
            'wolf',
            'bear',
            'dragon_face',
            'cactus']

        super().notify(
            ':{0}: {1}'.format(
                random.choice(emoticons),
                message),
            **kwargs)

    def hatch_pets(self):
        """ Hatch all available pets. """
        # first get the lists of things
        current_pets = self.get_pets(
            base=not self._config.no_base_pets,
            magic=self._config.magic_pets,
            quest=self._config.quest_pets,
            rare=False)

        potions = self.get_hatching_potions(
            base=True,  # we always need the base potions
            magic=self._config.magic_pets)

        eggs = self.get_eggs(
            base=not self._config.no_base_pets,
            quest=self._config.quest_pets)

        hatched = 0

        for egg, egg_quantity in eggs.items():
            for potion, potion_quantity in potions.items():
                potential_pet = '{0}-{1}'.format(egg, potion)

                if egg_quantity <= 0:
                    # logging.getLogger(__name__).debug(
                        # "Can't hatch %s, no egg", potential_pet)
                    continue
                if potion_quantity <= 0:
                    # logging.getLogger(__name__).debug(
                        # "Can't hatch %s, no potion", potential_pet)
                    continue
                if potential_pet in current_pets:
                    # logging.getLogger(__name__).debug(
                        # "Can't hatch %s, already have one", potential_pet)
                    continue

                try:
                    if self.dry_run:
                        response = {'message': 'dry run'}
                    else:
                        response = self._hs.hatch_pet(egg, potion)

                    logging.getLogger(__name__).info(
                        '%s: %s',
                        potential_pet,
                        response['message'])

                    hatched += 1
                    potions[potion] -= 1

                    # don't need to store the egg_quantity back into the dict,
                    # since it is the outer loop
                    egg_quantity -= 1

                    # strictly speaking don't need this either, since we
                    # shouldn't ever revist the same egg/potion combo
                    current_pets.append(potential_pet)
                except Exception as e:
                    logging.getLogger(__name__).warning(e)

        message = 'Hatched {0} new pets'.format(hatched)
        self.notify(message)
