#!/bin/bash

set -xeuf -o pipefail

sudo apt-get install -y tar build-essential lsb-release python3-pip python3-tk

pip3 install black
pip3 install flake8
