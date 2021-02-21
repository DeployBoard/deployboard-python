#!/bin/bash

# Used for github actions
BASEPATH='/github/workspace'

pip install -r ${BASEPATH}/src/api/requirements.txt
pip install -r ${BASEPATH}/src/web/requirements.txt
pip install -r ${BASEPATH}/tests/requirements.txt

pytest --cov-report html --cov-report xml --cov-report term --cov=src/ tests/
