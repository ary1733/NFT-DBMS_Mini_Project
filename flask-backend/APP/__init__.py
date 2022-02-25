from flask import Flask, url_for
from .routes import base_bp
# from flask_cors import CORS

# Main application and configuration
app=Flask(__name__)

# Maybe required in future
# cors = CORS(app)

# DB 



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
