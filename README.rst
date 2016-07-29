===============================
scriptabit
===============================

Python scripting for Habitica via the API

* Free software: Apache v2
* Homepage: https://github.com/DC23/scriptabit
* Documentation: https://scriptabit.readthedocs.org
* Version: 0.1.0

Installation
------------
::

    pip install scriptabit

Development
-----------

There is a makefile in the project root with targets for the most common
development operations such as lint checks, running unit tests, building the
documentation, and building installer packages. `tox` does not have a target,
as `make tox` is more typing than `tox`.

Run make with no target to see the list of targets::

    $ make

`Bumpversion <https://pypi.python.org/pypi/bumpversion>`_ is used to manage the
package version numbers. This ensures that the version number is correctly
incremented in all required files. Please see the bumpversion documentation for
usage instructions, and do not edit the version strings directly.

Version numbers follow the `Semantic versioning guidelines <semver.org>`_.
