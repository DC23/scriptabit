CSV Batch Upload
----------------

The `csv-tasks` plugin provides limited support for batch creation of Habitica
tasks from a CSV file. The supported task features are:

- Create habits, dailies, or todos
- task names
- task extra text
- difficulty level (trivial, easy, medium, or hard)
- character attribute (for attribute-based automatic levelling)
- tags
- for habits, the up and down scoring buttons can be specified.


Habitica task features that are **not currently supported** are:

- Due dates
- Checklists
- Custom rewards (actually they work now but the reward value is not set).

The CSV file must have a first row header, with the following columns:
  
- name (required): The task name
- type (required): must be either habit, daily, or todo
- description (optional): The extra notes
- priority (optional): Task difficulty. Should be one of trivial, easy, medium, or hard.
- attribute (optional): strength, intelligence, constitution, or perception.
- tags (optional): comma-separated list of tag names for each task
- up (optional): only used for habits. Any text at all here means the habit will have an up button.
- down (optional): only used for habits. Any text at all here means the habit will have an down button.
