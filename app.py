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
    'host': 'MY_HOST',
    'db': 'MY_DATABASE_NAME'
}

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
app.config['MAIL_SERVER'] = 'MAIL_SERVER_ADDRESS'
app.config['MAIL_PORT'] = // Mail port depends also if you use TLS or not, just put the number
app.config['MAIL_USE_TLS'] = // Set it to True or False
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER', 'MY_EMAIL_ADDRESS')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS', 'MY_EMAIL_PASSWORD')
mail = Mail(app)
