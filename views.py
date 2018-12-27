from flask import render_template, request, flash, redirect, request, url_for
from flask_login import login_user, UserMixin, current_user, login_required, logout_user
from app import db, app, login_manager, mail
from forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from flask_mail import Message
import bcrypt


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
            # exisisting_user = users.find_one({'email' : request.form['email']})
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
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # users = mongo.db.users
            # logging_user = users.find_one({'email' : request.form['email']})
            check_user = User.objects(email=form.email.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('profile'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    print('OK FATTO')

    form = UpdateAccountForm()
    # skform = AddNewSkill()
    # if skform.submit.data:
    #     User.objects(email=current_user.email).update_one(set__skills=current_user.skills+skform.skills.data, upsert=True)
    #     flash('Thanks for updating', 'success')

    # form.skills = current_user.skills
    if form.validate_on_submit():
        if form.picture.data:
            # picture_file = save_picture(form.picture.data)
            current_user.image_file = save_picture(form.picture.data)
            User.objects(email=current_user.email).update_one(set__image_file=current_user.image_file, upsert=True)
        User.objects(email=current_user.email).update_one(set__username=form.username.data, upsert=True)
        User.objects(email=current_user.email).update_one(set__skills=form.skills.data + form.owned_skills.data,
                                                          upsert=True)
        # Save the skills that the user already have and the new ones.
        flash('Thanks for updating', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        print('STAI NELL\'IF NELLA GET')
        form.owned_skills.data = current_user.skills
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename='img/' + current_user.image_file)
        return render_template('profile.html', title='Account', image_file=image_file, form=form)


@app.route('/validate', methods=['GET', 'POST'])
@login_required
def validate():
    return render_template('validate/index.html')


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='dibenedetto972@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RequestResetForm()
    if form.validate_on_submit():
        # user = User.query.filter_by(email=form.email.data).first()
        user = User.objects(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        User.objects(email=user.email).update_one(set__password=hashed_password)
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)