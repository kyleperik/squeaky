import socketio
import eventlet
import eventlet.wsgi
import werkzeug.serving

import redis

from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)
app.debug = True

db = redis.StrictRedis(host="localhost", port=6379, db=0)

@app.route('/')
def index():
    return render_template('index.html')

@sio.on('connect', namespace='/')
def connect(sid, environ):
    sio.emit('code', db.get('code').decode(), room=sid)

@sio.on('code change', namespace='/')
def code(sid, environ):
    db.set('code', environ['data'])
    sio.emit('code', db.get('code').decode(), skip_sid=sid)
    print('code_change', sid)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print('bubbles')
    print('disconnect', sid)

@werkzeug.serving.run_with_reloader
def run_server():
    sioapp = socketio.Middleware(sio, app)

    ws = eventlet.wsgi.server(eventlet.listen(('', 8080)), sioapp)
    ws.serve_forever()

if __name__ == '__main__':
    run_server()

