SHELL=/bin/sh
PACKAGE_NAME=scriptabit

.SILENT:
.IGNORE:

.PHONY: help
help:
	echo
	echo 'Utility Makefile for scriptabit'
	echo '============================'
	echo
	echo 'Targets supported are:'
	echo
	echo '  * clean: removes the build and directories, as well as __pycache__ and *.pyc files. Note that a clean also removes the generated documentation (as this is placed into build/docs).'
	echo '  * install-deps: installs development and test dependencies into your virtual environment.'
	echo '  * develop: installs scriptabit in development mode.'
	echo '  * uninstall: removes the development package from pip.'
	echo '  * tests: runs py.test.'
	echo '  * tests-slow: runs py.test, including slow tests.'
	echo '  * lint: runs pylint.'
	echo '  * lintr: runs pylint with a full report.'
	echo '  * html: builds the HTML documentation.'
	echo '  * pdf: builds the documentation in PDF format.'
	echo '  * latex: builds LaTeX source, used to generate other formats.'
	echo '  * alldocs: builds all documentation formats.'
	echo '  * sdist: builds a source distribution.'
	echo '  * bdist_wheel: builds a universal wheel distribution.'
	echo '  * register: register package with PiPY.'
	echo '  * upload: uploads a package to PiPY.'
	echo '  * tox: runs tox tests'

.PHONY: tox
tox:
	tox

.PHONY: tests
tests:
	py.test

.PHONY: tests-slow
tests-slow:
	py.test --runslow

.PHONY: clean
clean:
	echo Cleaning ...
	rm -rf build/ .tox/ ./setuptools-* .cache/
	find . -name "__pycache__" -nowarn -exec rm -rf {} \;
	find . -name "*.pyc" -nowarn -exec rm -rf {} \;
	find . -name "scriptabit.log" -nowarn -exec rm -rf {} \;
	echo ... done

.PHONY: install-deps
install-deps:
	pip install --upgrade pip setuptools
	pip install -e.[dev,test]

.PHONY: develop
develop: install-deps
	python setup.py develop

.PHONY: uninstall
uninstall:
	pip uninstall --yes $(PACKAGE_NAME)
	rm -rf *.egg-info/

.PHONY: lint
lint:
	pylint -rn ./$(PACKAGE_NAME)/

.PHONY: lintr
lintr:
	pylint -ry ./$(PACKAGE_NAME)/

.PHONY: sdist
sdist:
	python setup.py sdist

.PHONY: bdist_wheel
bdist_wheel:
	python setup.py bdist_wheel

.PHONY: html
html:
	sphinx-build -b html docs build/docs/html

.PHONY: latex
latex:
	sphinx-build -b latex docs build/docs/latex

.PHONY: pdf
pdf: latex
	$(MAKE) -C build/docs/latex all-pdf
	mkdir -p ./build/docs/pdf/
	mv build/docs/latex/*.pdf build/docs/pdf/

.PHONY: alldocs
alldocs: html latex pdf

.PHONY: register
register:
	python setup.py register

.PHONY: upload
upload: clean
	#python setup.py bdist_egg upload
	python setup.py sdist upload
