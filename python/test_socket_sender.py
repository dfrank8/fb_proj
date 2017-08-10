from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask("socket_testing")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def some_function():
    socketio.emit('some event', {'data': 42})

if __name__ == '__main__':
    # socketio.run(app)
    some_function()