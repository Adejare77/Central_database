""" Routing specifications for application"""
from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.forms import RegistrationForm
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.forms import EditProfileForm
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.forms import ResetPasswordForm
from app.user import MyUser

# NOTE: DUMMY DATA FOR DASHBOARD
headings = ('Database', 'Engine', 'Date Created')
databases = (
    ('Employees', 'MySQL', '2 years ago'),
    ('Users', 'MySQL', '1 year ago'),
    ('Products', 'MySQL', '10 months ago')
)

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home', headings=headings, databases=databases)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form, current_template='login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        MyUser().addUser(user.id)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, current_template='register.html')

@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template('user.html', user=user)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.email == form.email.data))
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

# INCOMPLETE
@app.route('/database_details/<database_name>')
def database_details(database_name):
    return render_template('details.html')

@app.route('/create_database', methods=['GET', 'POST'])
@login_required
def create_database():
    database_engines = ['MySQL', 'PostgreSQL', 'MongoDB']
    return render_template('database.html', title='Create Database', database_engines=database_engines)

@app.route('/submit_database_form', methods=['POST'])
@login_required
def submit_database_form():
    if request.method == 'POST':
        # Retrieve form data
        cluster_name = request.form.get('cluster_name')
        db_engine = request.form.get('db_engine')
        # Redirect to the dashboard page after form submission
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
