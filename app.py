from flask import Flask, g, abort, request
from flask_login import LoginManager, current_user
from config import Configuration
from flask_mongoengine import MongoEngine, Document
import os
from flask_bcrypt import Bcrypt
from flask_mail import Mail

app = Flask(__name__)

app.config.from_object(Configuration)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@app.before_request
def _before_request():
    g.user = current_user


app.config["MONGODB_SETTINGS"] = {
    'host': 'server',
    'db': 'pass'
}

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'secretkey'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'mail')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'pass')
mail = Mail(app)


@app.route('/add')
def add():
    user = mongo.db.users
    user.insert({'name': 'Anthony', 'cognome': 'cazzo'})

    return 'Added user!'
