CSV Batch Upload
----------------

Example command line::

    scriptabit --run csv_tasks --csv-file [my_csv_file]

The `csv-tasks` plugin provides limited support for batch creation of Habitica
tasks from a CSV file. The supported task features are:

- Create habits, dailies, todos, or rewards.
- task names
- task extra text
- difficulty level (trivial, easy, medium, or hard)
- character attribute (for attribute-based automatic levelling)
- tags
- for habits, the up and down scoring buttons can be specified.
- for rewards, the reward value can be specified.


Habitica task features that are **not currently supported** are:

- Due dates
- Checklists

The CSV file must have a first row header, with the following columns:

- name (required): Values are used for the task name.
- type (required): Values must be either habit, daily, or todo.
- description (optional): Values used as the extra notes.
- priority (optional): The task difficulty. Values should be one of trivial, easy, medium, or hard.
- attribute (optional): Values should be one of strength, intelligence, constitution, or perception.
- tags (optional): Values should be a comma-separated list of tag names for each task. Leave the entry blank if you don't want tags applied to a task.
- up (optional): This value is only used for habits. Any text at all here means the habit will have an up button.
- down (optional): This value is only used for habits. Any text at all here means the habit will have an down button.
- value (optional): Only used for rewards. Must be an integer value that is
  greater than zero. Used to set the value of the custom reward.
