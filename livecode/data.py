import redis

db = redis.StrictRedis(host="localhost", port=6379, db=0)

def get_code():
    return db.get('code').decode()

def set_code(code):
    return db.set('code', code)

def get_changeid():
    return db.get('changeid')

def get_change(id):
    return db.get(f'change:{id}')
