import wtforms
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SubmitField, FieldList
from wtforms_components import SelectMultipleField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError
from flask_login import current_user
from models import User
from flask_wtf import FlaskForm
import re

class LoginForm(Form):
	email = StringField("Email", validators= [validators.DataRequired()])
	password = PasswordField("Password", validators= [validators.DataRequired()])
	remember_me = BooleanField("Remember me?", default=True)


def validate(self):
	if not super(LoginForm, self).validate():
		return False

		self.email = User.authenticate(self.email.data, self.password.data)
		if not self.user:
			self.email.errors.append("Invalid email or password.")
			return False

		return True



class RegistrationForm(Form):
	name = StringField('Name', [validators.Regexp('^[A-Za-z]', message="Name must contains only letters")])
	surname = StringField('Surname', [validators.Length(min=4, max=25)])
	email = StringField('Email', validators= [validators.Length(min=6, max=35)])
	password = PasswordField('New Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Password must match')
		])
	confirm = PasswordField('Repeat Password')




class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(), validators.Length(min=2, max=20)])
    email = StringField('Email')
    # picture= FileField(u'Image File', [validators.regexp(u'^[^/\\\\]\.jpg$')])
    picture = FileField()
    # picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    skills = SelectMultipleField('Programming Language',
    	choices=(
            ('Programming Languages', (
            	('asm', 'Assembly'),
                ('c', 'C'),
                ('cpp', 'C++'),
                ('java', 'Java'),
                ('js', 'JavaScript'),
                ('sql', 'SQL'),
                ('plsql', 'PL/SQL'),
                ('python', 'Python'),
                ('php', 'PHP'),
                ('ruby', 'Ruby'),
                ('swift', 'Swift')
            )),
            ('Soft Skills', (
            	('pm', 'Project Management'),
                ('tw', 'Teamwork'),
                ('potato', 'Potato')
            ))
        ), render_kw={"data-placeholder": "Select all your skills..."})
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.objects(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

    # def validate_image(self, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

