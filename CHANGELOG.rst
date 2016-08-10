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

