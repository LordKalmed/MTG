#!/bin/bash

sudo apt install python3 python3-pip -y

pip install -r requirements.txt

export sqlhost="localhost"
export sqluser="root"
export sqlpass="root"
export sqldata="tournament"

echo 'TESTING:'
python3 -m pytest --cov=application --cov-report html

python3 app.py


