import socketio
import eventlet
import eventlet.wsgi
import werkzeug.serving

from livecode import data
from livecode import services
from livecode import models

from flask import Flask, render_template

sio = socketio.Server()
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@sio.on('connect', namespace='/')
def connect(sid, environ):
    sio.emit('code', data.get_code(), room=sid)
    print('connect', sid)

@sio.on('code change', namespace='/')
def code_change(sid, environ):
    last_changeid = environ['last_changeid']
    changes = [
        models.Change(
            line_from = change['from']['line'],
            char_from = change['from']['ch'],
            line_to = change['to']['line'],
            char_to = change['to']['ch'],
            text = change['text'],
        )
    for change in environ['changes']]
    result = services.transform(data.get_code(), changes)
    data.set_code(result)
    sio.emit('code change', changes, skip_sid=sid)
    print('code change', sid)

@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print('disconnect', sid)

@werkzeug.serving.run_with_reloader
def run_server():
    sioapp = socketio.Middleware(sio, app)

    ws = eventlet.wsgi.server(eventlet.listen(('', 8080)), sioapp)
    ws.serve_forever()

if __name__ == '__main__':
    run_server()

