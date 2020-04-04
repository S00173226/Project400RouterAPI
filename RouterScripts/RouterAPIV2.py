from flask import abort, request, make_response, Flask, jsonify
from flask_socketio import SocketIO, join_room, emit, send
import urllib3, requests, threading, json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'routerSecret!'
socketio = SocketIO(app)


@app.route('/registerDevice', methods=['POST'])
def registerDevice():
    return 'routerSecret!'

@socketio.on('test', namespace='/test')
def testing():
    emit('Working')









if __name__ == '__main__':
    socketio.run(app, debug=True)