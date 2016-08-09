Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

Bug reports
-----------

When `reporting a bug <https://github.com/DC23/scriptabit/issues>`_ please include:

    * Your operating system name and version.
    * Any details about your local setup that might be helpful in troubleshooting.
    * The scriptabit package version.
    * Detailed steps to reproduce the bug.

Documentation improvements
--------------------------

scriptabit could always use more documentation, whether as part of the official scriptabit docs, in docstrings, or even on the web in blog posts, articles, and such.

.. note:: This project uses Google-style docstrings.
   Contributed code should follow the same conventions.
   For examples, please see the `Napoleon examples
   <http://sphinxcontrib-napoleon.readthedocs.org/en/latest/example_google.html>`_,
   or the `Google Python Style Guide
   <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_.


Feature requests and feedback
-----------------------------

The best way to send feedback is to `file an issue <https://github.com/DC23/scriptabit/issues>`_

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Or, implement the feature yourself and submit a pull request.

Development
-----------

Setting up your Git Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To set up `scriptabit` for local development:

1. Fork the `scriptabit` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/scriptabit.git

3. Create a branch for local development::

    git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

4. When you're done making changes, run all the tests, doc builder and pylint
   checks::

    py.test
    pylint ./src/scriptabit/
    sphinx-build -b html docs build/docs

   Or, using the project makefile::

    make clean lint tests docs

5. Commit your changes and push your branch to GitHub::

    git add .
    git commit -m "Your detailed description of your changes."
    git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

The Development Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

I recommend using a Python virtual environment for development. Although not
essential, it is helpful to isolate the project from other Python packages that
may be installed. Once you create and activate the virtual environment, the
command `make develop` will install all the development dependencies and
`scriptabit` in develop mode. From then on, only changes to the setup files
(such as adding new entry points) will require rerunning the `make develop`
command. My method for setting up on Linux is basically::

    $ git clone https://github.com/DC23/scriptabit.git
    $ cd scriptabit
    $ mkvirtualenv -a . -p /usr/bin/python3 scriptabit
    $ workon scriptabit
    $ make develop
    $ make tests
    $ tox

The last two lines run all the tests, both directly in the dev virtual
environment and in tox against Python 2 and 3.

Pull Request Guidelines
-----------------------

If you need some code review or feedback while you're developing the code just make the pull request.

For merging, you should:

1. Include passing tests (run ``py.test``).
2. Update documentation when there's new API, functionality etc.
3. Add a note to ``CHANGELOG.rst`` about the changes.
4. Add yourself to ``AUTHORS.rst``.
