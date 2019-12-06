from flask import Flask, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__, static_folder=f"{url_for('static')}", template_folder=f"{url_for('templates')}")
app.config.from_object(Config)
app.secret_key = "something_only_you_know"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

from app import routes, models, errors