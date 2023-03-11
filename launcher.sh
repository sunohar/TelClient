#!/bin/sh
# launcher.sh
# Navigate to TelClient folder and execute script

# venv python
# cd /home/pi/Projects/TelClient
# . /home/pi/Projects/venv/383venv/bin/activate
# python -V
# python ./PyTelegram.py

# Pyenv python
cd /mnt/dietpi_userdata/Projects/TelClient
date
pwd
/home/dietpi/.pyenv/versions/ticsvenv/bin/python ./PyTelegram.py
