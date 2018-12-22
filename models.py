from flask_login import UserMixin
from app import db
from app import login_manager


class User(UserMixin, db.Document):
	meta = {'collection': 'users'}
	email = db.StringField(max_length=35)
	name = db.StringField(max_length=35)
	surname = db.StringField(max_length=35)
	password = db.StringField()
	username = db.StringField()
	image_file = db.StringField(nullable=False, default='static/img/default.jpg')
	skills = db.ListField(db.StringField())

@login_manager.user_loader
def load_user(user_id):
	return User.objects(pk=user_id).first()