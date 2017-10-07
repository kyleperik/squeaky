from livecode import models
import redis
import json

db = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_code():
    return db.get('code').decode()

def set_code(code):
    return db.set('code', code)

def get_changeid():
    return int(db.get('changeid').decode())

def get_changes(ids):
    if len(ids) == 0: return []
    result = [
        json.loads(c.decode())
    for c in db.mget([f'change:{id}' for id in ids])]
    return [
        models.Change(
            from_pos = models.Position(
                c['from']['line'],
                c['from']['ch'],
            ),
            to_pos = models.Position(
                c['to']['line'],
                c['to']['ch'],
            ),
            text = str.join('\n', c['text']),
        )
    for c in result]

def add_change(change):
    newid = db.incr('changeid')
    db.set(f'change:{newid}', json.dumps(change.serialize()))
    return newid
