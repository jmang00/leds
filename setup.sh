#!/bin/bash

echo "Installing dynamic leds - this may break other user installations.\n"

# Install dependencies
sudo apt-get update
sudo apt-get install python3-opencv
sudo apt-get install libopenblas-dev
sudo apt-get install libssl-dev
pip install pyyaml --break-system-packages
pip install adafruit-circuitpython-neopixel --break-system-packages
pip install RPi.GPIO --break-system-packages
pip install rpi_ws281x --break-system-packages
pip install numpy --break-system-packages
pip install requests --break-system-packages
pip install matplotlib --break-system-packages

# Define the alias line to add to .bashrc
alias_line="alias leds='/home/campi/leds/run.sh'"

# Check if the alias already exists to avoid duplicates
if ! grep -Fxq "$alias_line" ~/.bashrc
then
    # Add the alias to .bashrc
    echo "$alias_line" >> ~/.bashrc
    echo "Alias 'leds' added to .bashrc"
else
    echo "Alias 'leds' already exists in .bashrc"
fi

# old venv stuff:
# if ! [ -d venv ]; then
#   echo "Creating virtual environment..."
#   python3 -m venv venv
# fi

# cv2Path=$(python3 -c "import cv2; print(cv2.__file__)")

# if ! [ -d $cv2Path ] then
#     echo "Installing cv2 globally"
#     sudo apt-get update
#     sudo apt-get install python3-opencv
# else
#     echo "Found cv2 installed at $cv2Path, linking it."    
#     ln -s /usr/lib/python3/dist-packages/cv2.cpython-*.so venv/lib/python3.*/site-packages/
# fi

# source venv/bin/activate
# echo "Activated virtual environment: $(which python)"
# pip install pyyaml
# pip install adafruit-circuitpython-neopixel
# pip install RPi.GPIO
# pip install rpi_ws281x
# pip install numpy
# pip install requests
