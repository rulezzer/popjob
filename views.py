from flask import render_template, request, flash, redirect, request, url_for
from flask_login import login_user, UserMixin, current_user, login_required, logout_user
from app import app
from app import login_manager
from app import db
import bcrypt
from forms import LoginForm, RegistrationForm, UpdateAccountForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def homepage():
    name = request.args.get('name')
    if not name:
        name = '<unknown>'
    return render_template('homepage.html')


@app.route('/user_registration', methods=['POST', 'GET'])
def user_registration():
	form = RegistrationForm(request.form)
	if request.method == 'POST':
		if form.validate():
			# users = mongo.db.users
			#exisisting_user = users.find_one({'email' : request.form['email']})
			existing_user = User.objects(email=form.email.data).first()
			if existing_user is None:
				hashpass = generate_password_hash(form.password.data, method='sha256')
				user_creation = User(form.email.data, form.name.data, form.surname.data, hashpass).save()
				login_user(user_creation)
				flash('Thanks for registering')
				return redirect(url_for('login'))
	return render_template('user_registration.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated == True:
		return redirect(url_for('homepage'))
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate():
		#users = mongo.db.users
		# logging_user = users.find_one({'email' : request.form['email']})
			check_user = User.objects(email = form.email.data).first()
			if check_user:
				if check_password_hash(check_user['password'], form.password.data):
					login_user(check_user)
					return redirect(url_for('profile'))
	return render_template('login.html',form = form)


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('homepage'))


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	print ('OK FATTO')
	
	form = UpdateAccountForm(request.form)
	if form.validate_on_submit():
		
		User.objects(email=current_user.email).update_one(set__username=form.username.data, upsert=True)
		User.objects(email=current_user.email).update_one(set__skills=form.skills.data, upsert=True)
		
		flash('Thanks for updating', 'success')
		return redirect(url_for('profile'))
	elif request.method == 'GET':
		print('STAI NELL\'IF NELLA GET')
		form.username.data = current_user.username
		form.email.data = current_user.email

	return render_template('profile.html', form=form)