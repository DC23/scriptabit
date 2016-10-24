# Bootstrap setuptools with ez_setup. Wrapped in try as Tox and Travis CI don't
# like the bootstrapping code very much.
# Neither does readthedocs!

# on_rtd is whether we are on readthedocs.org,
# this line of code grabbed from docs.readthedocs.org
import os
import sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    try:
        import ez_setup
        ez_setup.use_setuptools()
    except Exception as exception:
        pass

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PyTest(TestCommand):

    """ Entry point for py.test that allows 'python setup.py test'
    to work correctly
    """

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='scriptabit',
    version='1.12.0',
    description='Python scripting for Habitica via the API',
    long_description=long_description,
    url='https://github.com/DC23/scriptabit',
    license='Apache 2.0',

    # Author details
    author='JugglinDan',
    author_email='jugglindan@gmail.com',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   1 - Planning
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        #   6 - Mature
        'Development Status :: 4 - Beta',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',

        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Games/Entertainment :: Role-Playing',
        'Topic :: Utilities',
    ],

    # What does your project relate to?
    keywords='Habitica, HabitRPG, Trello',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests']),

    include_package_data=True,

    cmdclass={'tests': PyTest},

    platforms='any',

    test_suite='tests.test_scriptabit',

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/technical.html#install-requires-vs-requirements-files
    install_requires=[
        'bidict',
        'configargparse',
        'configparser',
        'enum34',
        'future',
        'iso8601',
        'pytz',
        'py-trello',
        'requests',
        'tzlocal',
        'yapsy',
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [
            'bumpversion',
            'check-manifest',
            'ipython',
            'ipdb',
            'pylint',
            'sphinx',
            'sphinx_rtd_theme',
            'wheel',
        ],
        'test': [
            'pylint',
            'pytest',
            'pytest-sugar',
            'requests-mock',
            'tox',
            'virtualenv',
        ],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # Delete either or both of these if not required (and remove the corresponding imports in the package __init__.py
    entry_points={
        'console_scripts': [
            'scriptabit = scriptabit:start_scriptabit',
            'sb-banking = scriptabit:start_banking',
            'sb-csv = scriptabit:start_csv',
            'sb-health = scriptabit:start_health',
            'sb-pets = scriptabit:start_pets',
            'sb-trello = scriptabit:start_trello',
        ],
    },

    # Is your project zip safe?
    zip_safe=True,
)
