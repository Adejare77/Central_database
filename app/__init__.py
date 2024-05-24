from flask import Flask, Blueprint
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_session import Session
import os

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'your_secret_key_here'
Session(app)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
moment = Moment(app)


home = os.path.expanduser("~/Desktop")
users_path = os.path.join(home, "central_db", "all_users")
os.makedirs(users_path, exist_ok=True)

sqlite_path = os.path.join(home, "central_db", "sqlite_dbs")
os.makedirs(sqlite_path, exist_ok=True)

from app import routes, models, errors, routes_filters
