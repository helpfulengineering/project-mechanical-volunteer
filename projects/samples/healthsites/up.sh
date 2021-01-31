#!/bin/bash
pip install -r requirements.txt

currdir=$(pwd)

cd ../../..
source .env/bin/activate

cd ./backend/pybossa
docker build -t helpful-pybossa:latest .

cd $currdir
docker-compose up -d

python up.py

