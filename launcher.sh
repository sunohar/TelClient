#!/bin/sh
# launcher.sh
# Navigate to TelClient folder and execute script

# Normal python
# cd /home/pi/Projects/TelClient
# . /home/pi/Projects/venv/383venv/bin/activate
# python -V
# python ./PyTelegram.py

# Pyenv python
cd /mnt/dietpi_userdata/Projects/TelClient
python -V
pyenv which python
python ./PyTelegram.py