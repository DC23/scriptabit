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
* Version: 0.4.7

**Note** that apart from bugs, I don't use the GitHub issue list for
planning. Task and feature planning is carried out in a private
`Trello <https://trello.com>`_ board. Access can be provided on request.

Installation
------------
To install the latest release from `PyPI <https://pypi.python.org/pypi>`_:

::

    pip install scriptabit

You also require an authentication credentials file in your home directory
containing your
`Habitica API Key and User ID <https://habitica.com/#/options/settings/api>`__.
The file should have a typical ini file structure, with the following section:

::

    [habitica]
    userid = ; Paste your User ID here
    apikey = ; Paste your API key here

Additional sections can be added, and the section name to use can be
supplied as a command-line argument.

If you do not already have a `.auth.cfg` file, a default will be created when
you first run scriptabit. You can then fill in your account values.

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

After running `scriptabit` at least once, configuration files will be created in
`~/.config/scriptabit/`. These can be edited to change the default options. You
can revert to the installation defaults by deleting the files (they will be
recreated on the next run).

Writing Plugins
---------------

User plugins should be placed into the `scriptabit_plugins` directory. This
will be created in your home directory the first time `scriptabit` runs. Due to
an initialisation order issue, this directory location cannot be specified on
the command line (the plugin directory needs to be located before processing
command line arguments so that plugins get a chance to add additional
arguments). If the `SCRIPTABIT_USER_PLUGIN_DIR` environment variable is defined,
then this location will be used instead of the default location.

All plugins should subclass the `IPlugin` class. Refer to the API
documentation for details of the available methods.

Plugins use `Yapsy <http://yapsy.sourceforge.net/>`__, so all Yapsy
documentation is relevant to writing `scriptabit` plugins.
