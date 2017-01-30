Pet Care
--------

The Pet Care plugin streamlines a number of operations that are difficult to
carry out in large numbers through the current Habitica applications. Core
features are:

- `list-pets`: List current inventory of pet-related items. This is
  primarily for development support, as this task is easily achieved through the
  official applications.
- `feed-pets`: Batch pet feeding.
- `hatch-pets`: Batch pet hatching.

A number of flags exist to control the pets, food, and potions used for
the batch operations. They are:

- `any-pet-food`: If supplied, then all food types will be offered to all pets.
  The default behaviour is to only use the preferred foods for a pet. The main
  use of this flag is for the case where you have just a few pets, but a lot of
  food. It will let you raise the pets to a mount more quickly without having to
  wait for the preferred foods.
- `no-base-pets`: If supplied, then the standard pets will be excluded from
  batch operations, allowing you to focus on quest and magic potion pets.
  The default is to only feed standard pets.
- `quest-pets`: If supplied, quest pets will be included in batch operations.
  The default is to exclude quest pets.
- `magic-pets`: If supplied, magic potion pets will be included in batch
  operations. The default is to exclude magic potion pets.
- `no-raise`: If supplied, pets will not be raised to mounts during feeding.

Note that apart from the flags described above, you cannot control the order in
which pets are fed. Each pet will be repeatedly offered food until either the
(preferred) food is all gone, or the pet becomes a mount. If more food or pets
remain, then the process repeats. If you want to feed specific pets, this should
be done through the official applications.

Examples
++++++++

These example command lines all use the shortcut method. The long form would 
use `scriptabit --run pet_care` instead of `sb-pets`.

Feed preferred foods to standard pets only::

    sb-pets --feed-pets

Feed preferred foods to standard pets but do not raise to mounts::

    sb-pets --feed-pets --no-raise

Feed any food to quest pets only::

    sb-pets --feed-pets --no-base-pets --quest-pets --any-pet-food

Hatch all available standard pets::
    
    sb-pets --hatch-pets

Hatch all available standard and quest pets::
    
    sb-pets --hatch-pets --quest-pets
