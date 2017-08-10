from flask import Flask, render_template, render_template_string, request, redirect, Response, session, url_for, jsonify
from flask_socketio import SocketIO, send, emit
import pdb
import json
import urllib
import requests
import httplib2
import ast
import time
from pykeyboard import PyKeyboard
from AppKit import *
import threading
import collections

port = 8090
host = "localhost"

context = {}

app = Flask("ignite_hw_local")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='threading', ping_timeout=500, ping_interval=100)



def send_socket_message(channel, message):
    print("send_socket_message()")
    # socketio.run(app, port=socket_port)
    socketio.emit(channel, message)
    print("[x] Sent\t: ", message)

@socketio.on('context')
def handle_message(message):
    print("SOCKET - MESSAGE >>> MESSAGE")
    content = {}
    pb = NSPasteboard.generalPasteboard()
    pb.clearContents()
    k = PyKeyboard()
    highlighted_text = ""
    all_text = ""
    # k.press_keys(['Command', 'a'])
    k.press_keys(['Command', 'c'])
    time.sleep(.2)
    content["highlighted_text"] = pb.stringForType_(NSStringPboardType)
    time.sleep(.2)
    # k.press_keys(['Command', 'a'])
    # time.sleep(.2)
    # k.press_keys(['Command', 'c'])
    # time.sleep(.2)
    # content["entire_text"] = pb.stringForType_(NSStringPboardType)
    print("HERE IS THE CONTENT >>>" + str(content))
    send_socket_message("context", content)
    return content
from pynput.keyboard import Key, Listener

shortcuts_launch = ['ctrl','shift','d']
down_keys = []

def on_press(key):
    global down_keys
    # if hasattr(key, 'char'):
    #     down_keys.append(str(key.char))
    if hasattr(key, 'name'):
        # down_keys.append(str(key.name))
        if(str(key.name) == "cmd"):
            send_socket_message("window", "show")
    # if(collections.Counter(shortcuts_launch) == collections.Counter(down_keys)):
    #     send_socket_message("show_window","")
    # else:
    #     print(down_keys)

def on_release(key):
    global down_keys
    # if hasattr(key, 'char'):
    #     if(str(key.char) in down_keys):
    #         down_keys.remove(str(key.char))
    if hasattr(key, 'name'):
        if(str(key.name) == "cmd"):
            send_socket_message("window", "hide")
    # if(collections.Counter(shortcuts_launch) == collections.Counter(down_keys)):
    #     print ("Please hide window")
        
        down_keys=[]

def thread1():
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
            listener.join()

threading.Thread(target = thread1).start()
# Collect events until released

    
socketio.run(app, host="localhost", port=8090)
