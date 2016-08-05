# -*- coding: utf-8 -*-
""" PyCharm needs a script to serve as an entry point for debugging.
The actual scriptabit.py does not work due to relative imports
(which are quite legal inside the package).
This script lives outside the scriptabit package and acts as a proxy to
the actual entry point."""

from scriptabit import start_cli

if __name__ == "__main__":
    start_cli()
