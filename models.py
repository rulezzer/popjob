from flask_login import UserMixin
from mongoengine import DateTimeField

from app import db, app
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = db.StringField(max_length=35)
    data = DateTimeField()
    email_confirmation_sent_on = db.StringField(date=None, nullable=True)
    email_confirmed = db.BooleanField(default=False)
    email_confirmed_on = db.StringField(date=None, nullable=True)
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


class Company(UserMixin, db.Document):
    meta = {'collection': 'company'}
    email = db.StringField(max_length=35)
    password = db.StringField()
    confirm = db.StringField()
    nation_type = db.StringField()
    NameCompany = db.StringField()
    PartitaIva = db.StringField()
    Telefono = db.StringField()
    NameResponsabile = db.StringField()
    SurnameResponsabile = db.StringField()

#
# @login_manager.user_loader
# def load_company(user_id):
#     return Company.objects(pk=user_id).first()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
