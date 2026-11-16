# Meeting-Summariser
A Meeting Summariser for the Raspberry Pi 4 that uses a USB microphone to record audio and summarise it using ollama qwen3:0.6b

# How to Use
First navigate into the folder meetingsum and create a venv with python:

<img width="390" height="30" alt="image" src="https://github.com/user-attachments/assets/fa2330e3-63d5-47fc-8180-f4d5cd50ca0f" />

Then navigate into the venv with <code>source ./venv/bin/activate</code>:

<img width="445" height="33" alt="image" src="https://github.com/user-attachments/assets/ef186d10-ee2d-40d8-a5c6-2d7aa68dfb00" />

Next install all the requirements in requirements.txt by using <code>pip install -r requirements.txt</code>

Now you can plug in a USB microphone into one of the Pi 4's USB ports and run main.py. You will be prompted to press space to start recoding, this will not work in SSH unless you physically plug a separate keyboard into it and use Space on that.

# Compatibility
This Project is for the Raspberry Pi 4 and has been tested on Raspberry Pi OS Lite.
