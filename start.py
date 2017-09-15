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
    print('connect', sid)

def transform(lines, changes):
    '''make changes to lines of text'''
    if len(changes) == 0: return lines
    change = changes[0]
    before = str.join('\n',
        lines[:change['from']['line']]
        + [lines[change['from']['line']][:change['from']['ch']]]
    )
    replaced = str.join('\n', change['text'])
    after = str.join('\n',
        [lines[change['to']['line']][change['to']['ch']:]]
        + lines[change['to']['line'] + 1:]
    )
    result = str.join('', [before, replaced, after])
    return transform(str.split(result, '\n'), changes[1:])

@sio.on('code change', namespace='/')
def code(sid, environ):
    changes = environ['changes']
    lines = str.split(db.get('code').decode(), '\n')
    result = str.join('\n', transform(lines, changes))
    db.set('code', result)
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

