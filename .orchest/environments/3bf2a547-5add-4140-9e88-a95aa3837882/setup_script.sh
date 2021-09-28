#!/bin/bash

# Install any dependencies you have in this shell script.

# E.g. pip install tensorflow

cpwd=$(pwd)
cd ~
pip install -e "git+https://github.com/orchest/orchest.git#egg=orchest&subdirectory=orchest-sdk/python"
cd $cpwd

pip install -r requirements.txt
pip list
