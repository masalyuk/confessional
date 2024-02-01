#/bin/sh!
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git
sudo apt-get install python
sudo apt-get install python3-pip

sudo apt-get install baresip
sudo apt-get install ffmpeg
sudo apt-get pulseaudio 

sudo apt-get install libasound2-dev

# need to activate python env
pip3 install -r requirements.txt
