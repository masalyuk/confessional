#!/bin/bash

# Update and upgrade system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
sudo apt-get install -y git python python3-pip baresip ffmpeg pulseaudio libasound2-dev

# Activate an existing virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Virtual environment 'venv' does not exist. Creating a new one..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install Python dependencies from requirements.txt
pip3 install -r requirements.txt

# Deactivate the virtual environment
deactivate

echo "Script completed."
