Readme
======

Python scripting and scenarios for Habitica.

.. image:: https://img.shields.io/travis/DC23/scriptabit.svg
    :target: https://travis-ci.org/DC23/scriptabit
    :alt: Travis CI

.. image:: https://readthedocs.org/projects/scriptabit/badge/?version=latest
    :target: http://scriptabit.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/l/scriptabit.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: Apache 2.0 License

.. image:: https://img.shields.io/pypi/v/scriptabit.svg
    :target: https://pypi.python.org/pypi/scriptabit
    :alt: PyPI

.. image:: https://img.shields.io/pypi/pyversions/scriptabit.svg
    :target: https://www.python.org

* Free software: Apache 2.0
* Homepage: https://github.com/DC23/scriptabit
* Documentation: https://scriptabit.readthedocs.org
* Version: 1.18.0

**Note** You can use the Github issues for bugs and feature requests, however
most task and feature planning is carried out in a private
`Trello <https://trello.com>`_ board. Access can be provided on request.

Installation
------------
To install the latest release from `PyPI <https://pypi.python.org/pypi>`_::

    pip install scriptabit

If you already have `scriptabit` installed, then upgrade with::

    pip install --upgrade scriptabit

Habitica Credentials
++++++++++++++++++++
You require an authentication credentials file in your home directory
containing your
`Habitica API Key and User ID <https://habitica.com/#/options/settings/api>`__.
The file should have a typical ini file structure, with the following section::

    [habitica]
    userid =
    apikey =

Additional sections can be added, and the section name to use can be
supplied as a command-line argument.

If you do not already have a `.auth.cfg` file, a default will be created when
you first run scriptabit. You can then fill in your account values.

Once you have entered your Habitica credentials, test them with the `-sud`
command (short for `--show-user-data`)::

    scriptabit -sud

If everything is set up correctly, you should see a summary of your character
data printed to the console.

**Note that your API key is effectively a password to your Habitica
account.** You should make sure the .auth.cfg file is protected, and
never share the key with others. On Linux and related systems, you can
set the permissions as follows::

    chmod 600 .auth.cfg

.. _trello-credentials:

Trello Credentials
++++++++++++++++++
If you wish to use the Trello plugin, you will need to add your Trello
credentials to the .auth.cfg file as follows::

    [trello]
    apikey =
    apisecret =
    token =
    tokensecret =

Your API key and API secret can be
`obtained here <https://trello.com/1/appKey/generate>`_.

Your authorisation token and token secret will be obtained through an
interactive process when you first run the trello plugin. You must first save
your API key and API secret to the .auth.cfg file before you will be able to
obtain the token and tokensecret.

.. _usage:

Usage
-----

`scriptabit` is a command-line application. Help on the available commands can
be obtained by running::

    $ scriptabit --help

Operations include:

- `-sud`: Show user data.
- `-hp n`: Set the user health to n
- `-mp n`: Set the user's mana points to n
- `-xp n`: Set experience points to n
- `-gp n`: Set gold to n
- `-ls`: List available plugins.

After running `scriptabit` at least once, configuration files will be created in
`~/.config/scriptabit/`. These can be edited to change the default options. You
can revert to the installation defaults by deleting the files (they will be
recreated on the next run).

See the :ref:`detailed-usage` section for detailed instructions on specific
functionality.

Finally, most of the built-in plugins define a convenience command-line
application name:

- `sb-banking` is a shortcut for `scriptabit --run banking`
- `sb-csv` is a shortcut for `scriptabit --run csv_tasks`
- `sb-health` is a shortcut for `scriptabit --run health_effects`
- `sb-pets` is a shortcut for `scriptabit --run pet_care`
- `sb-trello` is a shortcut for `scriptabit --run trello`
- `sb-tasks` is a shortcut for `scriptabit --run tasks`

When using the shortcuts, all other command-line arguments are the same as when
running `scriptabit`.

Notification Panel
++++++++++++++++++

By default, most scriptabit operations update a scoreless habit in Habitica with
some status information. This can be useful when you have some functions running
in an update loop.

The use of this panel can be controlled with the ``use-notification-panel``
argument, either on the command line or by setting a value into the
scriptabit.cfg file. Set to 0 or False to suppress the panel.

Habitica Tags
+++++++++++++

By default, scriptabit applies the `scriptabit` tag to all the tasks it creates
in Habitica. This behaviour can be controlled with the ``--tags`` option. It
accepts a comma-separated list of tags.

To disable the use of tags, set the option to an empty string: ``--tags ""``

Writing Plugins
---------------

User plugins should be placed into the `scriptabit_plugins` directory. This
will be created in your home directory the first time `scriptabit` runs. Due to
an initialisation order issue, this directory location cannot be specified on
the command line (the plugin directory needs to be located before processing
command line arguments so that plugins get a chance to add additional
arguments). If the `SCRIPTABIT_USER_PLUGIN_DIR` environment variable is defined,
then this location will be used instead of the default location.

**Note that plugin data files may also be written to the user plugin directory**

All plugins should subclass the `IPlugin` class. Refer to the API
documentation for details of the available methods.

Also refer to the API documentation (and the view source option) for the
sample plugin which can be used as a template for new plugins.
