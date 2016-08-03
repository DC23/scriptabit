Readme
======

Python scripting and scenarios for Habitica.

.. image:: https://travis-ci.org/DC23/scriptabit.svg?branch=master
    :target: https://travis-ci.org/DC23/scriptabit
    
.. image:: https://readthedocs.org/projects/scriptabit/badge/?version=latest
    :target: http://scriptabit.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

* Free software: Apache 2.0
* Homepage: https://github.com/DC23/scriptabit
* Documentation: https://scriptabit.readthedocs.org
* Version: 0.2.1

Roadmap
-------

The next utility function planned is the ability to feed all food in the
inventory to an appropriate pet (by default only the main pets, but optionally
feeding quest pets as well or instead). While this won't let you control the
specific pet that gets fed, it will be useful when a lot of food has
accumulated.

The first planned scenario will implement a poisoning, and health regen script.
As part of the development of the poisoning scenario, the following features
will be added to the code:

* Plugin framework using `Yapsy <http://yapsy.sourceforge.net/>`__

    * This will give the ability to load and run user-defined scenarios.

* Ability to chain scenarios together into a composite operation.
* Build toolkit of useful scenario building blocks:

    * Detect task activity
    * Detect skill and reward use (health potions, skills)
    * Detect "perfect day" buff status

**Note** that apart from bugs, I don't use the GitHub issue list for
planning. Task and feature planning is carried out in a private 
`Trello <https://trello.com>`_ board. Access can be provided on request.

Installation
------------
Note that the code is not yet in `PyPI <https://pypi.python.org/pypi>`_, 
so until then cloning this repo and using setuptools to install is your 
best option.

::

    pip install scriptabit

You also require an authentication credentials file containing your
`Habitica API Key and User
ID <https://habitica.com/#/options/settings/api>`__. The default is to
look for this information in ~/.auth.cfg, but a different path can be
specified on the command line (or in the ini file). The file should have
a typical ini file structure, with the following section:

::

    [habitica]
    userid = ; Paste your User ID here
    apikey = ; Paste your API key here

Additional sections can be added, and the section name to use can be
supplied as a command-line argument.

**Note that your API key is effectively a password to your Habitica
account.** You should make sure the .auth.cfg file is protected, and
never share the key with others. On Linux and related systems, you can
set the permissions as follows:

::

    chmod 600 .auth.cfg

Usage
-----

`scriptabit` is a command-line application. Help on the available commands can
be obtained by running::

    $ scriptabit --help

Functionality is of two major types: single operations (utility functions)
that complete quickly, and scenarios that will cause scriptabit to run until
killed. Currently only a few operations are available, and no scenarios.
Operations include:

- `-sud`: Show user data.
- `-hp n`: Set the user health to n
- `-mp n`: Set the user's mana points to n
- `-xp n`: Set experience points to n

There are commands to list available scenarios, and to run a scenario, but they
have no effect in this version.
