from flask import Flask
from flask_socketio import SocketIO, rooms, emit, join_room
from flask_cors import CORS
from config import Config

app = Flask(__name__)

#CORS(app)
#cors = CORS(app, resources={r"/connections/*": {"origins": "*"}})
socketio = SocketIO(app)
socketio.rooms = rooms

from app import routes