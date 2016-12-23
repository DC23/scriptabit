Tasks Plugin
------------

Example command line::

    sb-tasks --list-tasks

The ``tasks`` plugin provides a collection of task manipulation functions.
For batch upload of tasks from a CSV file, please see the ``csv-tasks`` plugin.
The supported task features are:

- ``--list-tasks``
  List the tasks. If the ``--verbose`` option is specified, then a full data dump
  of the tasks is made. Otherwise just the names are listed.
- ``--delete-tasks``
  Deletes all tasks of the specified type.

Options are:

- ``--verbose``: Verbose output.
- ``--task-type``: Specify the type of task to operate on. Values are `habits`,
  `dailys`, `todos`, `rewards`, or `all`.
