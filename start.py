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
    sio.emit('last changeid', data.get_changeid(), room=sid)
    print('connect', sid)

@sio.on('code change', namespace='/')
def code_change(sid, environ):
    last_changeids = [
        change['last_changeid']
    for change in environ['changes']]
    changes = [
        models.Change(
            from_pos = models.Position(
                change['from']['line'],
                change['from']['ch'],
            ),
            to_pos = models.Position(
                change['to']['line'],
                change['to']['ch'],
            ),
            text = str.join('\n', change['text']),
        )
    for change in environ['changes']]
    new_code = services.transform(data.get_code(), changes)
    data.set_code(new_code)
    current_changeid = data.get_changeid()
    new_changes = [
        services.apply_change(c[0], c[1], current_changeid)
    for c in zip(changes, last_changeids)]
    print(new_changes)
    sio.emit('last changeid', data.get_changeid(), room=sid)
    result_changes = [
        c.serialize()
    for c in new_changes]
    sio.emit('code change', result_changes, skip_sid=sid)

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

