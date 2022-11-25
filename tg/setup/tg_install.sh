#!bin/bash

# Ensure we are running as root
if [ "$EUID" -ne 0 ]
  then echo "This script must run as root."
  exit
fi

# Install python3
apt-get install -y python3 python3-pip || { echo "Failure"; exit 1; }

# Install Pipenv
pip3 install --user pipenv || { echo "Failure"; exit 1; }

# Install Python dependencies with pipenv
python3 -m pipenv install || { echo "Failure"; exit 1; }

# Install TRex
bash ../trex/trex_installer.sh 2.92 || { echo "Failure"; exit 1; }
