from flask_login import UserMixin
from app import db, app
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=35)
    name = db.StringField(max_length=35)
    surname = db.StringField(max_length=35)
    password = db.StringField()
    username = db.StringField()
    image_file = db.StringField(nullable=False, default='static/img/default.jpg')
    skills = db.ListField(db.StringField())
    owned_skills = db.ListField(db.StringField())

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'email': self.email}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            email = s.loads(token)['email']
        except:
            return None
        return User.objects.get(email=email)

    def __repr__(self):
        return f"User('{self.username}','{self.email}', '{self.image_file}')"


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
