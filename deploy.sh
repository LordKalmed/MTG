#!/bin/bash

sudo apt install python3 python3-pip -y

pip3 install -r requirements.txt

echo 'TESTING:'
python3 -m pytest --cov=application --cov-report html

python3 app.py