#!/bin/bash
#
# NOTE: requires virtualenvwrapper
#
git submodule init
git submodule update --recursive
mkvirtualenv nose2
pip install -r requirements.txt
python setup.py develop
