#!/bin/bash

#python3.6 -m venv venv
#source venv/bin/activate
pip install -r requirements.txt
echo "export PYTHONPATH=\"${PYTHONPATH}:${PWD}\"" >> ~/.bash_profile
echo "export PRIVGUARD=\"${PWD}\"" >> ~/.bash_profile
source ~/.bash_profile
echo "Setup complete"