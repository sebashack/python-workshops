#!/bin/bash

set -xeuf -o pipefail

sudo apt-get install -y tar build-essential lsb-release python3-pip

pip3 install black
pip3 install flake8
