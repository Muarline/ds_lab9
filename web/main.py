# from https://codeburst.io/building-your-first-chat-application-using-flask-in-7-minutes-f98de4adfa5d
import os
from flask import Flask, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

app = Flask(__name__)
socketio = SocketIO(app)

mongo_client = MongoClient(os.environ.get('DB_URI'))
database = mongo_client.chat

while True:
    try:
        mongo_client.admin.command('ismaster')
    except ConnectionFailure:
        pass
    else:
        break

@app.route('/')
def sessions():
    return render_template('session.html')

@socketio.on('initialize')
def handle_initialization(data):
    uid = data['uid']
    for document in database.messages.find({}):
        data = {
            'username': document['username'],
            'message': document['message']
        }
        socketio.emit(f'receive_message_{uid}', data)

@socketio.on('send_message')
def handle_message_sending(data):
    database.messages.insert_one(data.copy())
    socketio.emit('receive_message', data)

socketio.run(app, host='0.0.0.0', port=8888)
