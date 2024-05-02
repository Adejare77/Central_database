#!/usr/bin/python3

from flask import Flask, jsonify, make_response
from flask_session import Session
from app.v1.views import central_db
from app.v1.views.login import *
from app.v1.views.database import *

app = Flask(__name__)

app.register_blueprint(central_db)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_secret_key_here'
Session(app)

@app.errorhandler(404)
def error_404(e):
    return make_response(jsonify({"error": "Not found"}))



if __name__ == "__main__":
    app.run(debug=True)
