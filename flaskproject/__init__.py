from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskproject.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail=Mail(app)

from flaskproject.users.routes import users
from flaskproject.requests.routes import requests
from flaskproject.main.routes import main
from flaskproject.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(requests)
app.register_blueprint(main)
app.register_blueprint(errors)