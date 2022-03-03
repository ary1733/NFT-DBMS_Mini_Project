from functools import wraps
from flask import redirect, url_for, session, request, make_response, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def api_session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is None:
            return make_response(jsonify({"message": "session not found"}), 200)
        return f(*args, **kwargs)
    return decorated_function