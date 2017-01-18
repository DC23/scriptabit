Changelog
=========

0.1.0 (2016-07-29)
-----------------------------------------

* First version
* Generated project boiler plate with `cookiecutter <https://github.com/audreyr/cookiecutter>`_
  and the `cookiecutter-dcpypackage <https://github.com/DC23/cookiecutter-dcpypackage>`_
  template.
* Adjusted the cookiecutter output.

0.2.0 (2016-08-03)
-----------------------------------------

* First version that does anything useful :)
* Documentation cleaned up
* CI builds in Travis.
* Documentation on ReadTheDocs
* Authentication from .auth.cfg file
* Command-line interface established
* Unit tests with pytest and requests_mock
* Utility functions to set HP, MP, and XP.

0.2.2 (2016-08-07)
-----------------------------------------

* Fixes issue #2 by adding a multipath search for configuration files.

0.2.3 (2016-08-07)
-----------------------------------------

* Fixed issue #3 (broken Travis builds) by making setuptools bootstrap more
  robust.
* Cleaned up authentication file handling - generate default, more error checks.
* Moved utility function CLI arg definitions into the utility functions class.

0.3.0 (2016-08-10)
-----------------------------------------

* Implemented plugin framework.
* Added test utility function. The functionality of this will change all the
  time, depending on my current test needs.
* Changed scenario text to reference plugins instead.
* Added max-updates command line argument.

0.4.0 (2016-08-11)
-----------------------------------------

* Implemented banking plugin.
* Fixed issue where the app would sleep after updating a plugin even when no
  more updates were required.
* Added task upsert method to HabiticaService.

0.4.1 (2016-08-11)
-----------------------------------------

* Updated documentation to include the built-in plugins.

0.4.2 (2016-08-11)
-----------------------------------------

* Minor documentation fixes.

0.4.3 (2016-08-11)
-----------------------------------------

* Restructured the documentation layout. I think this has better organisation
  of the indices and TOCs.

0.4.4 (2016-08-11)
-----------------------------------------

* Updated status to alpha
* Fixed bug with bank task name being overwritten.
* Refactored HabiticaService upsert method
* Added create_task and get_task methods to HabiticaService

0.4.5 (2016-08-12)
-----------------------------------------

* Added to PyPI
* Fixes issue #5 (missing files in PyPI package)

0.4.6 (2016-08-12)
-----------------------------------------

* Fixes issue #6 (missing plugin metadata files in PyPI package)

0.4.7 (2016-08-12)
-----------------------------------------

* Changed default logging options to be less intrusive.
* A lot of fixes to datetime handling, which should fix #7

0.5.0 (2016-08-16)
-----------------------------------------

* Fixed load-order issue for configuration files. Who would have thought that
  configargparse started looking for configuration files from the end of the
  list rather than the start?
* Started adding Trello sync plugin. Doesn't really do much yet, but all the
  authentication song and dance code is in place, as well as configuration for
  defining which boards to sync, the lists on those boards, and the optional
  lists that will indicate task completion.
* Implemented core functionality for task synchronisation between generic
  task services.

1.0.0 (2016-08-17)
-----------------------------------------

* Fixed task sync bug with missing destination tasks.
* HabiticaService now supports a task filter on get_tasks
* Implemented Habitica sync task
* Implemented HabiticaTaskService
* Updated documentation with sync information
* Implemented first version of Trello to Habitica sync. Tasks only, no
  difficulties, attributes, due-dates or checklists.

1.1.0 (2016-08-17)
-----------------------------------------

* Trello sync now uses optional Trello labels to indicate Habitica task
  difficulty and character attribute (strength, perception, intelligence,
  constitution). If they don't exist, the labels are created automatically.
* Habitica cards are now created with a "Trello" tag.
* Added due date synchronisation support.

1.2.0 (2016-08-18)
-----------------------------------------

* Made sync data file name into a trello plugin argument
* Refactored task sync class into smaller functions that make the logic easier
  to read and modify.
* Added last_modified property to Task (and TrelloTask, HabiticaTask)
* Added modification time check for deciding whether to update tasks
* Added persistence for last sync time
* Improved sync stats reporting

1.3.0 (2016-08-19)
-----------------------------------------

* Refined sync log message levels to reduce the spam at info levels
* Added notification ability by using a scoreless habit whose text can be
  updated by scriptabit functions.
* Added notifications to banking and trello plugins.
* Added global command-line argument for specifing the update interval of
  looping plugins.
* Implemented ability to set default difficulty and character attribute for
  cards on a Trello board.
* Implemented ability to sync all cards on a board, or just those assigned to
  the current user.
* Minor bug fixes, and lint warning cleanups.

1.4.0 (2016-08-22)
-----------------------------------------

* Added checklist support to Trello sync
* Added CSV batch task creation plugin.
* Slightly improved error handling during task sync. Now an error in a task
  doesn't bring the whole sync down. Instead it logs the error and skips to the
  next task.
* Made sync of task description/extra text optional, with default to False.

1.5.0 (2016-08-24)
-----------------------------------------

* Updated usage documentation for banking, and CSV upload.
* Added transaction fee option to banking functions.
* Added tax feature to banking plugin.
* Added direct gold amount setting to utility functions (-gp X)
* Changed bank fees to use a diminishing returns function, to reward the larger
  risk of saving longer to deposit larger amounts.

1.6.0 (2016-08-25)
-----------------------------------------

* Added pet feeding function to pet care plugin.
* Trello cards that are both new and completed are now synchronised to Habitica
  if their last update time is more recent than the last synchronisation.
* Added support for a 'no sync' label on Trello cards. Cards with this label are
  ignored even if they meet all the other criteria for synchronisation.
* Added pet care usage documentation.

1.7.0 (2016-08-26)
-----------------------------------------

* Added trello plugin usage documentation.
* Added pet hatching function to pet care plugin.
* Updated documentation.

1.7.1 (2016-08-29)
-----------------------------------------

* Fixed #13: incorrect pet count when API error occurs.
* Made pet-care commands more logical (issue #16)
* Fixed issue #14: trying to feed pet when mount already exists.
* Fixed issue #15: errors if config and user plugin directories don't exist on
  first run (when depth is > 1)
* Added note to CSV plugin docs indicating that Daily repeat options are not
  supported.

1.8.0 (2016-08-29)
-----------------------------------------

* Added messages and checks for dry run support in plugins.
* Implemented full dry run mode support in banking.
* Implemented full dry run mode support in CSV uploader.
* Implemented full dry run mode support in pet care plugin.
* Implemented full dry run mode support in trello sync plugin.
* Implemented full dry run mode support in the utility functions.
* Updated utility functions so they return the new value set into the character
  stats (gold, XP, HP, MP).

1.8.1 (2016-08-29)
-----------------------------------------

* Added missing supports_dry_run method to pet care plugin, that was preventing
  dry runs.
* Fixed incorrect dryrun message in main loop.

1.9.0 (2016-08-30)
-----------------------------------------

* Updated documentation.
* Added new entry points for built-in plugins:

    * `sb-banking` instead of `scriptabit --run banking`
    * `sb-trello` instead of `scriptabit --run trello`
    * `sb-pets` instead of `scriptabit --run pet_care`
    * `sb-csv` instead of `scriptabit --run csv_tasks`
    * `sb-health` instead of `scriptabit --run health_effects`

1.10.0 (2016-08-30)
-----------------------------------------

* Made plugin update more robust. Exceptions are caught so that updates can
  continue rather than aborting the whole run.
* Implemented simple health drain and regeneration in health effects plugin.
* Refactored plugin notification methods.
* Changed pet care so it only sleeps during feeding if API calls were made
  during the last pet.

1.11.0 (2016-09-20)
-----------------------------------------

* Minor logging changes: config file specifiable via environment variable
  (`SCRIPTABIT_LOGGING_CONFIG`). Log statement with the location of the user
  plugin directory.
* Added 10 second timeout to http requests.
* Added simple vampire mode - health drain during the day, slower regen at
  night.
* Added bank-balance option so that sb-banking with no args can display usage
  information.
* Changed main loop so that utility functions don't try to run at the same time
  as plugins.
* Removed upper MP limit check when setting mana.
* Added delete all todos utility function (can update to support other task
  types later, but todos is all I needed right now).
* Fixed bug where last Trello sync time was displayed in UTC rather than local
  time.

1.12.0 (2016-10-24)
-----------------------------------------

* Updated pet care to handle the candy foods.
* Updated pet care to handle the spooky and ghost potions.
* Added purchase armoire item utility function, with optional repeat.

1.12.1 (2016-10-24)
-----------------------------------------

* Fixed bug in `--any-pet-food` feeding option in pet-care plugin.

1.12.2 (2016-10-31)
-----------------------------------------

* Added dry run support to armoire purchases
* Added 2 second delay between repeated armoire purchases.

1.12.3 (2016-11-25)
-----------------------------------------

* Made timestamp optional for all notification messages.

1.13.0 (2016-12-02)
-----------------------------------------

* Added spell/skill casting function.

1.13.1 (2016-12-02)
-----------------------------------------

* Added list all tasks function

1.14.0 (2016-12-09)
-----------------------------------------

* Added spellcast plugin

1.14.1 (2016-12-21)
-----------------------------------------

* Added HP preservation option to spellcast plugin. This allows casting Blessing
  spells that don't heal the player.

1.15.0 (2016-12-22)
-----------------------------------------

* Adding increment functions for XP, MP, HP. I already have direct set functions
  but the new ones are easier when you just want to increment the values up or
  down.
* Expanding the banking feature to allow mana and health banks as well as gold.
* Removed the bank name option, as it made supporting different bank types more
  complicated.

1.16.0 (sometime in January 2017)
-----------------------------------------

* New tasks plugin. Run with ``sb-tasks``.
* Added minimum requests version to setup.py.
* Added entry point for spellcasting plugin ``sb-cast``.
* Cleaned up argument parsing, so running a plugin entry-point with the --help
  argument only shows help for that plugin.
* Running ``scriptabit --help`` now only shows help for the main application
  rather than all possible args from all plugins.
* Added documentation for spell casting.
* Added fallback help display so that plugins that fail to define a ``print_help``
  function will use the default help display.

1.17.0 (Monday January 16, 2017)
-----------------------------------------

* Changed pet_care logic so it detects quest and magic pets implicitly. This
  means I don't need to manually update the code for new quest or magic pets.
* Added tag management features to ``sb-tasks``. You can now list tags, list
  unused tags, and delete unused tags. I didn't add a function to delete a tag
  by name as this is trivial to do in the web app.
* Fixed the issue in 1.16.0 where plugin names would log as "None".
* Added sample task CSV file showing the required layout for ``sb-csv``
* Updated documentation for pet care and tasks.

1.17.2 (Tuesday January 17, 2017) 
-----------------------------------------

* Very minor changes to PyPI metadata and README file.
* Made the update and creation of the notification panel optional. Use the
  `use-notification-panel` command line argument to control the behaviour.
* Made the task tags configurable. Use the ``--tags`` argument to pass a comma
  separated list of tags that will be used with any task created in Habitica. If
  you use ``--tags ""`` then no tags will be created or applied.
