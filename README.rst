======
Readme
======

Python scripting and scenarios for Habitica.

Roadmap
-------
The first version will be hard-coded with a single scenario - poisoning.
For a later version I plan to use `Yapsy <http://yapsy.sourceforge.net/>`_ to 
implement a plugin framework. This will allow scenarios to be defined as Python
scripts in a configurable directory. These plugins will be able to leverage the
common framework. How much value this will be is unclear.

Installation
------------
::

    pip install scriptabit

You also require an authentication credentials file containing your 
`Habitica API Key and User ID <https://habitica.com/#/options/settings/api>`_.
The default is to look for this information in `~/.auth.cfg`, but a different 
path can be specified on the command line (or in the ini file).
The file should have a typical ini file structure, with the following section::

    [habitica]
    userid = ; Paste your User ID here
    apikey = ; Paste your API key here

Additional sections can be added, and the section name to use can be supplied as
a command-line argument.

**Note that your API key is effectively a password to your Habitica account.**
You should make sure the `.auth.cfg` file is protected, and never share 
the key with others. On Linux and related systems, you can set the permissions
as follows::

    chmod 600 .auth.cfg

Usage
-----
To do.
