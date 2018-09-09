#!/bin/bash

# Create the VPP startup config file
cp ./startup.conf /etc/vpp/startup.conf

# start vpp
service vpp start

