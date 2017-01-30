.. _detailed-usage:

Working with User Stats
-----------------------

Basic user stats can be displayed with the ``--show-user-data`` 
(short form ``-sud``) command:

    ``scriptabit -sud``

Additionally, gold, mana, health, experience points, and character level can all
be modified with ``set``, ``increment``, and ``scale`` commands.  The ``set``
commands set the values directly, the ``increment`` commands add or subtract the
specified amount from the current value, and the ``scale`` commands multiply the
current value by the supplied scaling factor.

The ``set`` commands all have the form ``--set-XX``, where XX is one of:

- gp: gold points
- hp: health points
- mp: mana points
- xp: experience points
- level: character level

The ``increment`` commands all have the form ``--inc-XX``, using the same codes.

The ``scale`` commands all have the form ``--scale-XX``, using the same codes.

Example 1: subtract 10 health points
====================================
Use an increment command for hp, and a value of -10 to reduce health by 10 points:

    ``scriptabit --inc-hp -10``

Example 2: Set gold to 1000
===========================
Use the set command for gp, and a value of 1000:

    ``scriptabit --set-gp 1000``

Example 3: Reduce experience points by half
===========================================
Use a scale command on XP:

    ``scriptabit --scale-xp 0.5``

Using the Built-in Plugins
--------------------------

Some features of scriptabit are more complex than setting HP via the command
line. These features are described in more detail here.

.. toctree::
    :maxdepth: 1
    :glob: 
    
    *
