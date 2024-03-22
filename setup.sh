#!/bin/bash

#python3.6 -m venv venv
#source venv/bin/activate
pip install -r requirements.txt
echo "export PYTHONPATH=\"${PYTHONPATH}:${PWD}\"" | sudo tee -a ~/.bash_profile > /dev/null
echo "export PRIVGUARD=\"${PWD}\"" | sudo tee -a ~/.bash_profile > /dev/null
echo "Setup complete"