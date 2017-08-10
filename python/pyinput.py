from pynput.keyboard import Key, Listener
import pdb
import collections

shortcuts_launch = ['ctrl','shift','d']
down_keys = []

def on_press(key):
    if hasattr(key, 'char'):
        down_keys.append(str(key.char))
    if hasattr(key, 'name'):
        # down_keys.append(str(key.name))
        if(str(key.name) == "cmd")
    if(collections.Counter(shortcuts_launch) == collections.Counter(down_keys)):
        print("COMBO")
    else:
        print(down_keys)

def on_release(key):
    if hasattr(key, 'char'):
        if(str(key.char) in down_keys):
            down_keys.remove(str(key.char))
    if hasattr(key, 'name'):
        if(str(key.name) in down_keys):
            down_keys.remove(str(key.name))
    # if key == Key.esc:
    #     # Stop listener
    #     return False

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()