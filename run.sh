#!/usr/bin/env bash

if [[ $1 = "first" ]]
then
    echo "setting up virtual environment"
    virtualenv env
    source env/bin/activate

    echo "installing requirements"
    pip install -r requirements.txt
fi

# run local server
python todoapp.py
