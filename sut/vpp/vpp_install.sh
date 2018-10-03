#!/bin/bash

# Install VPP configuration tool
apt-get install python-pip
pip install vpp-config

# Install VPP  with APT (Latest Released Version)
touch /etc/apt/sources.list.d/99fd.io.list
echo "deb [trusted=yes] https://nexus.fd.io/content/repositories/fd.io.ubuntu.xenial.main/ ./" | sudo tee -a /etc/apt/sources.list.d/99fd.io.list
apt-get update

apt-get install vpp-lib
apt-get install vpp
apt-get install vpp-plugins
