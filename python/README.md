# Dependencies
* brew
* Python

## Installation
Python install
```
pip install -r requirements.txt
```

Edit in `loca_server.py` near line 59 `ser_port = '/dev/cu.usbmodem1411'` to the actual serial port. This can be found in the Arduino IDE app under `tools > Port`.

Or using terminal `ls /dev/tty.*`.

## Running it
To run the script

- You need to install virtualenv if you haven't already by running `pip install virtualenv`

- Once you have installed virtualenv, you need to create a virtual environment for the first(& last) time `virtualenv ./venv`

- Now, you need to activate the virtual environment you already created by running `source ./venv/bin/activate`. At this point, you should see *(venv)* preceding your prompt at the terminal, this means you're in the virtual environment now.

- If you're installing the virtual environment for the first time, you need to install the packages as well. To do that run `pip install -r requirements.txt`

- Proceed to run the local server by `python3 local_server.py`

NOTE: If you have already installed the virtual environment once, you don't need to install the packages again. Simply activate the virtual environment by running `source ./venv/bin/activate` and then proceed to run the local server.

- If you need to exit the virtual environment, run `deactivate`. At this point *(venv)* would no longer appear before the prompt.

## Killing it
To kill Python
```
kill $(pgrep -f "Python3 local_server.py")
```
