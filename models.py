from flask_login import UserMixin
from mongoengine import DateTimeField, EmbeddedDocumentListField, EmbeddedDocument, StringField, BooleanField, ListField

from app import db, app
from app import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Cskills(EmbeddedDocument):
    skillName = StringField()
    date = DateTimeField()
    status = BooleanField()

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    email = StringField(max_length=35)
    data = DateTimeField()
    email_confirmation_sent_on = StringField(date=None, nullable=True)
    email_confirmed = BooleanField(default=False)
    email_confirmed_on = StringField(date=None, nullable=True)
    name = StringField(max_length=35)
    surname = StringField(max_length=35)
    password = StringField()
    username = StringField()
    image_file = StringField(nullable=False, default='default.jpg')
    owned_skills = ListField(StringField())
    kskills = EmbeddedDocumentListField(Cskills)



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
    email = StringField(max_length=35)
    password = StringField()
    confirm = StringField()
    nation_type = StringField()
    NameCompany = StringField()
    PartitaIva = StringField()
    Telefono = StringField()
    NameResponsabile = StringField()
    SurnameResponsabile = StringField()

#
# @login_manager.user_loader
# def load_company(user_id):
#     return Company.objects(pk=user_id).first()


@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()
