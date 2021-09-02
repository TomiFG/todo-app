#!/usr/bin/env bash

# create and activate an environment called env
virtualenv env
source env/bin/activate

# install requirements
pip install -r requirements.txt

# run local server
python todoapp.py
