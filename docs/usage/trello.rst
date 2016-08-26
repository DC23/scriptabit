Trello
------

The `trello` plugin provides synchronisation (currently only one-way) from
Trello cards to Habitica todos. Key features are:

- Sync selected Trello boards and lists (selectable by name)
- Sync all cards on a board, or just those assigned to you (good for shared
  boards)
- Use Trello labels to control the Habitica todo difficulty and character
  attribute (useful when using automatic attribute point assignment). The
  required labels will be created if necessary by the trello plugin. The labels
  are created with no color in Trello so they won't interfere with any existing
  labels, but the color can be changed in Trello if desired.
- Use a 'no sync' label on cards to prevent synchronisation of that card even if
  it meets all the other criteria for synchronisation.
- The Python script can run in a loop, checking for changes every 30 minutes by
  default (but this is adjustable).
- The default task difficulty and character attribute can be set per board.
- Cards that have already been seen are remembered between runs, so after the
  first synchronisation the updates will be a lot faster.

The following features are synchronised on each card:

- Name.
- Description. Optional, off by default.
- Due date.
- Checklists.
- Difficulty (trivial, easy, medium, hard) via Trello labels.
- Character attribute.
- Completion status.

Configuration
+++++++++++++

Refer to the :ref:`trello-credentials` section of the README for instructions on
configuring authentication with your Trello account.

Although configuration options for boards and lists can be supplied on the
command line, they are best set in the scriptabit configuration file. See the
:ref:`usage` section for general information on the configuration file,
including its default location. Only Trello specific options are discussed here.

This is a typical configuration file section for the trello plugin::

    [trello]
    # Specify default settings for each board by specifying a composite string:
    #    board_name|difficulty|attribute|user
    # If you do not specify the difficulty then it defaults to easy.
    # If you do not specify the attribute then it defaults to strength.
    # If you don't specify anything for the user field, it defaults to using all
    # cards on the board.
    # E.G.:
    trello-boards = [Work|easy|intelligence|user, scriptabit|easy|intelligence]
    trello-lists = [Next Actions, Waiting For, Scheduled, Backlog, Doing]
    trello-done-lists = [Done]

Boards
^^^^^^

Boards are specified by name, with additional board options specified in the
composite string. The format is `Board name|default difficulty|default
attribute|user`. If the difficulty is not specified it defaults to easy, and if
the attribute is not specified it defaults to strength. This matches the
Habitica defaults.

Legal values for difficulty are:

- trivial
- easy
- medium
- hard

Legal values for attribute are:

- strength
- intelligence
- perception
- constitution

Invalid values will cause a warning, and the default values will be used
instead.

Finally, note that the order of board options is fixed. So if you want to
specify an attribute default, you must also specify the preceeding difficulty.

Lists
^^^^^

Lists are also specified by name. `trello-lists` defines the list names that
will be searched for incomplete cards, while `trello-done-lists` defines the
names of the lists that indicate completed cards. See :ref:`donelists` for
details on the use of Done lists as opposed to archiving cards.

.. _donelists:

Done Lists versus Archiving: A Note on Task Completion in Trello
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The concept of a card being completed doesn't really exist in Trello. Two
possibilities of marking a Trello card as complete are archiving the card, or
moving it to a Done list. For efficiency reasons, the scriptabit trello plugin
requires that you use a Done list. Archived cards are never seen by scriptabit,
so if you archive a card then the trello plugin will think the card has been
deleted rather than completed. The key reason for this behavior is that Trello
boards can easily have thousands of archived cards, and checking all of these on
every synchronisation would be very slow. The Trello API does not supply
a method to only retrieve cards that were archived within the last day or so.
I have therefore chosen to treat a configurable list as indication that a card
is "done". Once the cards in the Done list have been synchronised to Habitica
they can then be archived in Trello without consequences.

Example Command Lines
+++++++++++++++++++++

Run the trello plugin with default options::

    scriptabit --run trello

Run once rather than syncing every 30 minutes::

    scriptabit --run trello --max-updates 1
