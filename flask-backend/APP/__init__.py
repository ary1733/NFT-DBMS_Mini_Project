from flask import Flask, url_for, g
from .routes import base_bp
from APP.utils import query_db, get_db, SCHEMA

# from flask_cors import CORS

# Main application and configuration
app=Flask(__name__)

# Maybe required in future
# cors = CORS(app)
app.register_blueprint(base_bp, url_prefix="/api")

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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
    


@app.route("/map")
def get_map():
    data={}
    for rule in app.url_map.iter_rules():
        try:
            data[str(rule.endpoint)]=str(url_for(rule.endpoint))
        except:
            pass
    return data
