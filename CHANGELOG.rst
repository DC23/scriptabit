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
