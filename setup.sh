#!/bin/zsh

#python3.6 -m venv venv
#source venv/bin/activate
pip install -r requirements.txt
echo "export PYTHONPATH=\"${PYTHONPATH}:${PWD}\"" | sudo tee -a ~/.zprofile > /dev/null
echo "export PRIVGUARD=\"${PWD}\"" | sudo tee -a ~/.zprofile > /dev/null
echo "Setup complete!"
echo "I am going to exit in a few seconds."
echo "If your env vars are not set yet, please run 'source ~/.zprofile' to apply the changes."
sleep 5
exit