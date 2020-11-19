#!/bin/bash
pip install -r requirements.txt

currdir=$(pwd)

cd ../../../backend/pybossa
docker build -t helpful-pybossa:latest .

cd $currdir
docker-compose up -d

python up.py

