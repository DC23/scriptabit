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
- ``--list-tags``
  List all tags.
- ``--list-unused-tags``
  List all tags that are not assigned to any tasks.
- ``--delete-unused-tags``
  Delete all tags that are not assigned to any tasks. Note that if the
  ``dry-run`` flag is also given, this will revert to simply listing the unused
  tags.
    

Options are:

- ``--verbose``: Verbose output.
- ``--show-uuid``: Show the task UUID when listing tasks.
- ``--task-type``: Specify the type of task to operate on. Values are `habits`,
  `dailies`, `todos`, `rewards`, or `all`.
- ``--dry-run``: List the actions that would be carried out, but don't change
  anything on the server.
