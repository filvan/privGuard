#!/bin/zsh

#python3.6 -m venv venv
#source venv/bin/activate
pip install -r requirements.txt
echo "export PYTHONPATH=\"${PYTHONPATH}:${PWD}\"" | sudo tee -a ~/.zprofile > /dev/null
echo "export PRIVGUARD=\"${PWD}\"" | sudo tee -a ~/.zprofile > /dev/null
. ~/.zprofile
echo "Setup complete"