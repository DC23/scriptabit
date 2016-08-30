Health Effects
--------------

The Health Effects plugin currently provides simple implementations of
poisoning/health-draining and health regeneration. The longer-term plan for this
plugin is to provide a more complex scenario of poisoning and health
regeneration effects that are based on your performance on Dailies and Habits.
Custom rewards will also be created to implement cures that can be purchased in
game.

Examples
++++++++

Drain 15 HP over 24 hours, updating every 30 minutes::

    sb-health --update-frequency 30 --max-hp-change-per-day 15 --health-drain

Regenerate 10 HP over 24 hours, updating every 30 minutes (shortcut args)::

    sb-health -uf 30 -hp24 10 --health-regen
