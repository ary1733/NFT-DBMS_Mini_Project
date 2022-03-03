from flask import Flask, redirect, url_for, g, render_template, session
from .routes import base_bp
from APP.utils import query_db, get_db, SCHEMA
import os

# from flask_cors import CORS

# Main application and configuration
app = Flask(__name__)

# For Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
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
    # for user in query_db('select * from user'):
    #     print(user)
    # return query_db('select * from user')
    # return "Hi"
    return render_template("base.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
    
@app.route('/account')
def account():
    return render_template("account.html")

@app.route("/map")
def get_map():
    data={}
    for rule in app.url_map.iter_rules():
        try:
            data[str(rule.endpoint)]=str(url_for(rule.endpoint))
        except:
            pass
    return data
