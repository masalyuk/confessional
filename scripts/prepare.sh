#/bin/sh!
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install git
sudo apt-get install python

sudo apt-get install baresip
sudo apt-get install ffmpeg
sudo apt-get pulseaudio 

# need to activate python env
pip3 install -r requirements.txt

#.venv/lib/python3.10/site-packages/baresipy/__init__.py
#  def convert_audio(input_file, outfile=None):
# change sample rate to 8k
# channels 1
# due audiocode


sudo apt-get install libasound2-dev


