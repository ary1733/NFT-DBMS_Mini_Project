from flask import Flask, url_for, g
from .routes import base_bp
import sqlite3

# from flask_cors import CORS

# Main application and configuration
app=Flask(__name__)

# Maybe required in future
# cors = CORS(app)

# DB 
DATABASE = './APP/Database/mysql.db'
SCHEMA = './Database/mysql.sql'

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    print(g.__dict__)
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()





def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    # cur = get_db().cursor()
    for user in query_db('select * from user'):
        print(user)
    # return query_db('select * from user')
    return "Hi"
    


app.register_blueprint(base_bp)
@app.route("/map")
def get_map():
    data={}
    for rule in app.url_map.iter_rules():
        try:
            data[str(rule.endpoint)]=str(url_for(rule.endpoint))
        except:
            pass
    return data
