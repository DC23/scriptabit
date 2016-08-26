Pet Care
--------

The Pet Care plugin streamlines a number of operations that are difficult to
carry out in large numbers through the current Habitica applications. Core
features are:

- `pets-list-items`: List current inventory of pet-related items. This is
  primarily for development support, as this task is easily achieved through the
  official applications.
- `pets-feed`: Batch pet feeding.
- `pets-hatch`: Batch pet hatching.

A number of flags exist to control the pets, food, and potions used for
the batch operations. They are:

- `pets-any-food`: If supplied, then all food types will be offered to all pets.
  The default behaviour is to only use the preferred foods for a pet. The main
  use of this flag is for the case where you have just a few pets, but a lot of
  food. It will let you raise the pets to a mount more quickly at the cost of
  more food.
- `no-base-pets`: If supplied, then the standard pets will be excluded from
  batch operations, allowing you to focus on quest and magic potion pets.
  The default is to only feed standard pets.
- `quest-pets`: If supplied, quest pets will be included in batch operations.
  The default is to exclude quest pets.
- `magic-pets`: If supplied, magic potion pets will be included in batch
  operations. The default is to exclude magic potion pets.

Note that apart from the flags described above, you cannot control the order in
which pets are fed. Each pet will be repeatedly offered food until either the
(preferred) food is all gone, or the pet becomes a mount. If more food or pets
remain, then the process repeats. If you want to feed specific pets, this should
be done through the official applications.

An example command line to feed preferred foods to standard pets::

    scriptabit --run pet_care --pets-feed

A command line to feed any food to quest pets only::

    scriptabit --run pet_care --pets-feed --no-base-pets --quest-pets

A command line to hatch all available standard pets::
    
    scriptabit --run pet_care --pets-hatch

A command line to hatch all available standard and quest pets::
    
    scriptabit --run pet_care --pets-hatch --quest-pets
