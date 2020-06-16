#!/usr/bin/env bash
## Description:
##  Script to build the docker image.
##
## Usage: ./run_tests.sh

pipenv install --dev

# install package in "editable" mode to enable testing using a src layout where the
# application root package resides in a sub-directory (allows to test the "installed" version)
pipenv run python setup.py develop

# run unit tests and collect coverage data
pipenv run coverage run --source=src -m pytest -v

# report code coverage
pipenv run coverage report -m