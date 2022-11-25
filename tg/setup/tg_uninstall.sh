#!bin/bash

# Ensure we are running as root
if [ "$EUID" -ne 0 ]
  then echo "This script must run as root."
  exit
fi

# Remove Python environment
python3 -m pipenv uninstall
