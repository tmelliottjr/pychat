import json
from flask import request, jsonify
from app import app, socketio, emit, join_room
from werkzeug.contrib.cache import MemcachedCache
cache = MemcachedCache(['127.0.0.1:11211'])

@app.route('/connections', methods=['GET'])
def connections():
  return "str"
  #return jsonify(get_verified_connections()), 200


@socketio.on('disconnect')
def disconnect():
  connections = cache.get('connections')
  
  try:
    name = connections[request.sid]
  except KeyError:
    return

  del connections[request.sid]

  cache.set('connections', connections)

  if name:
    payload = [
      name,
      get_verified_connections()
    ]
  
    socketio.emit('user-disconnected', payload)

@socketio.on('connect')
def connect():
  connections = cache.get('connections')

  if connections is None:
    connections = {}
  
  connections[request.sid] = None

  name = request.args.get('name')
  sid = request.sid

  if name in connections.values():
    socketio.emit('connection-error','Username already taken.', room=sid)
    return

  connections[sid] = name

  cache.set('connections', connections)

  payload = [
    name,
    get_verified_connections()
  ]

  socketio.emit('user-connected', payload)
  emit('connection-success','success')

@socketio.on('client-message')
def client_message(msg):

  connections = cache.get('connections')

  name = connections[request.sid]

  socketio.emit('message', {'name': name, 'message': msg})

def get_verified_connections():
  connections = cache.get('connections')

  if connections is None:
    connections = {}

  verifiedConnections = {}
  
  for sid, name in connections.items():
    if name:
      verifiedConnections[sid] = name
  
  return verifiedConnections