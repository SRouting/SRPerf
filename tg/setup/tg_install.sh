#!bin/bash

# Ensure we are running as root
if [ "$EUID" -ne 0 ]
  then echo "This script must run as root."
  exit
fi

# Install python3
apt-get install -y python3 python3-pip

# Install Pipenv
pip3 install --user pipenv

# Install Python dependencies with pipenv
python3 -m pipenv install

# Install TRex
bash ../trex/trex_installer.sh 2.92
