from flask import Flask, g, abort, request
from flask_login import LoginManager, current_user
from config import Configuration
from flask_mongoengine import MongoEngine, Document 

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_object(Configuration)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def _before_request():
	g.user = current_user


app.config["MONGODB_SETTINGS"] = {
	'host': 'mongodb://phaeena:chuck00@ds121182.mlab.com:21182/tecweb',
	'db': 'tecweb'
} 

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/add')
def add():
	user = mongo.db.users
	user.insert({'name' : 'Anthony', 'cognome': 'cazzo'})

	return 'Added user!'