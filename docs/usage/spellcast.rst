Spell/Skill Casting Plugin
--------------------------

The ``spellcast`` plugin allows you to cast skills/spells. Some spells require
a target (eg: the Rogue Backstab skill). For these skills, you need to supply
the Habitica unique ID of the target (the UUID). 

This plugin is primarily intended for use from scripts, as obtaining the
required UUIDs and entering them on the command line is error prone and tedious.

Example command line::

    sb-cast --cast-skill toolsOfTrade

You can obtain the UUID of a task by using the tasks plugin
to list tasks with the ``show-uuid`` or ``verbose`` flags::

    sb-task --list-tasks --show-uuid

If using the ``verbose`` flag, all information will be displayed.
The ``id`` or ``_id`` field contains the required value.

For casting skills on other party members, you can obtain the player UUID from
the Habitica web client.

Example showing backstab being cast three times on a task::

    sb-cast --cast backStab --target 7b069a9e-80aa-47ab-99fd-15fae4dd8ba7 -n 3

Options are:

- ``--preserve-user-hp``: For spells that modify health, this option will
  preserve the player's original health value. This only works with the Blessing
  skill (``healAll``), allowing the player to heal the party but not themselves.
- ``-n N``: An optional count (defaults to 1). Skills will be cast N times, or
  until mana is exhausted.
