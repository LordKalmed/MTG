#!/bin/bash

sudo apt install python3 python3-pip -y

pip3 install -r requirements.txt

export sqlhost="localhost"
export sqluser="root"
export sqlpass="root"
export sqldata="tournament"

echo 'TESTING:'
python3 -m pytest --cov=application --cov-report html

python3 app.py


create table player (pid int, name char(25), surname char(25), email char(50), age int)
create table score (pid int, score1 int, score2 int, score3 int, score4 int)