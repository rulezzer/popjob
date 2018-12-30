from flask import Flask, g
from flask_login import LoginManager, current_user
from config import Configuration
from flask_mongoengine import MongoEngine
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
    'host': 'my_db_host',
    'db': 'my_db_name'
}

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'my_mail')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'my_pass')
mail = Mail(app)
