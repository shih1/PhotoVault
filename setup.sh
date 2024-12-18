#!/bin/bash

# Ensure pip3 is up to date
python3 -m pip install --upgrade pip

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

echo "Dependencies have been installed successfully."
