#!/bin/bash

. env/bin/activate
apt-get -qq -y install apt-transport-https ca-certificates
pip install --upgrade MySQL-python mysql-connector
pip install --upgrade -r requirements.txt -t lib

export FLASK_ENV=development
export FLASK_APP=app.python
flask run --host=0.0.0.0

eval "$@"
