from datetime import datetime
import bcrypt, os, secrets
from flask import render_template, request, flash, redirect, url_for, render_template, make_response
from flask_login import login_user, current_user, login_required, logout_user
from app import app, login_manager, mail
from forms import LoginForm, RegistrationForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, RegCompanyForm, \
    SearchSkillsForm, RemoveSkillsForm
from models import User, Company, Cskills
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
import pdfkit


@app.route('/index')
@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/user_registration', methods=['POST', 'GET'])
def user_registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        if form.validate():
            existing_user = User.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                user_creation = User(email=form.email.data, name=form.name.data, surname=form.surname.data,
                                     password=hashpass).save()
                print('3')
                login_user(user_creation)
                # User.objects(email=user_creation.email).update(set__username=str(user_creation.id)) #set the username equal to the id
                # send_confirmation_email(form.email.data)
                print('d')
                flash('Thanks for registering!  Please check your email to confirm your email address.', 'success')
                return redirect(url_for('login'))
            else:
                flash('User already registered for this email', 'danger')
    return render_template('user_registration.html', form=form)


# @app.route('/confirm/<token>')
# def confirm_email(token):
#     user = User.verify_reset_token(token)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('homepage'))
#         user = User.objects(email=user.email).first()
#         if user.email_confirmed:
#             flash('Account already confirmed. Please login.', 'info')
#         else:
#             user.email_confirmed = True
#             user.email_confirmed_on = datetime.now()
#         flash('Your email has been confirmed! ', 'success')
#         return redirect(url_for('login'))
#     return render_template('profile.html')
# try:
#     confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
# except:
#     flash('The confirmation link is invalid or has expired.', 'error')
#     return redirect(url_for('users.login'))
#
# user = User.query.filter_by(email=email).first()
#
# if user.email_confirmed:
#     flash('Account already confirmed. Please login.', 'info')
# else:
#     user.email_confirmed = True
#     user.email_confirmed_on = datetime.now()
#     db.session.add(user)
#     db.session.commit()
#     flash('Thank you for confirming your email address!')
#
# return redirect(url_for('recipes.index'))


# def send_confirmation_email(user):
#     token = user.get_reset_token()
#     msg = Message('Confirm Email', sender='dibenedetto972@gmail.com', recipients=[user.email])
#     msg.body = f'''To confirm your email, visit the following link:
#         {url_for('confirm', token=token, _external=True)}
#         If you did not make this request then simply ignore this email and no changes will be made.
#     '''
#     mail.send(msg)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('homepage'))
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(email=form.email.data).first()
            check_company = Company.objects(email=form.email.data).first()

            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('homepage'))
            elif check_company:
                if check_password_hash(check_company['password'], form.password.data):
                    login_user(check_company)
                    return redirect(url_for('homepage'))
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
@app.route('/profile/', methods=['GET', 'POST'])
@app.route('/profile/me', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    formRM = RemoveSkillsForm()
    select = request.form.get('skillRemoveSelect')

    if request.method == 'POST' and request.form['btn'] == 'Remove':
        print("removing skill " + select)
        User.objects(email=current_user.email).update(pull__kskills__skillName=select)
        return redirect(url_for('profile'))

    elif request.method == 'POST' and request.form['btn'] == 'Update':
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
            User.objects(email=current_user.email).update_one(set__image_file=current_user.image_file, upsert=True)
        User.objects(email=current_user.email).update_one(set__username=form.username.data, upsert=True)
        return redirect(url_for('profile'))


    elif request.method == 'POST' and request.form['btn'] == 'Save':
        flag = False
        for lol in form.skills.data:
            if User.objects(email=current_user.email, kskills__skillName__ne=lol):
                utente = User.objects(email=current_user.email).get()
                utente.kskills.append(Cskills(skillName=lol, status=False, date=datetime.now()))
                utente.save()
                flag = True
            else:
                flash(lol + ' is already present', 'danger')
        if flag:
            flash('Thanks for updating', 'success')

            # Save the skills that the user already have and the new ones.
        return redirect(url_for('profile'))
    elif request.method == 'GET':

        formRM.skillRemove = form.owned_skills
        form.owned_skills.data = [y.skillName for y in
                                  current_user.kskills]  # take the skillName from mongodb and pass them to the form
        formRM.skillRemove.data = form.owned_skills.data
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for('static', filename='img/' + current_user.image_file)

        return render_template('profile.html', title='Account', image_file=image_file, form=form, formRM=formRM)


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


# Skill's search
@app.route('/searchskills', methods=['GET', 'POST'])
@login_required
def searchskills():
    form = SearchSkillsForm(request.form)
    if request.method == 'POST':

        x = User.objects(kskills__skillName=form.skills.data).all()

        return render_template('searchskills.html', form=form, x=x)
    elif request.method == 'GET':
        return render_template('searchskills.html', form=form)


# Company Registration
@app.route('/company_registration', methods=['POST', 'GET'])
def company_registration():
    form = RegCompanyForm(request.form)
    if request.method == 'POST':
        if form.validate():
            existing_user = Company.objects(email=form.email.data).first()
            if existing_user is None:
                hashpass = generate_password_hash(form.password.data, method='sha256')
                hey1 = Company(form.email.data, hashpass, hashpass, form.nation_type.data, form.NameCompany.data,
                               form.PartitaIva.data,
                               form.Telefono.data, form.NameResponsabile.data, form.SurnameResponsabile.data).save()
                login_user(hey1)
                flash('Thanks for registering')
                return redirect(url_for('login'))
    return render_template('company_registration.html', form=form)


@app.route('/profile/<id>', methods=['POST', 'GET'])
def profileView(id):
    form = UpdateAccountForm()
    profile = User.objects(id=id).first()
    form.owned_skills.data = [y.skillName for y in profile.kskills]  # take the skillName from mongodb and pass them to the form
    form.username.data = profile.username
    form.email.data = profile.email
    return render_template('profile_view.html', form=form, profile=profile)


@app.route('/profile/<id>/cv')
def pdf_template(id):
    profile = User.objects(id=id).first()
    pro_pic = url_for('static', filename='img/' + profile.image_file)


    rendered = render_template('pdf_template.html', profile=profile, pro_pic=pro_pic)
    css = ['templates/css/cv_pdf_template.css']
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'

    return response
