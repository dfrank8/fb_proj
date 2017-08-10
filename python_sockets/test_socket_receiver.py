from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode="threading")

@socketio.on('channel-a')
def channel_a(message):
    '''
    Receives a message, on `channel-a`, and emits to the same channel.
    '''
    print "[x] Received\t: ", message

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, port=7001)