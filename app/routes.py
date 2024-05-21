#!/usr/bin/python3
""" Routing specifications for application"""
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_user
import sqlalchemy as sa
from app.forms import RegistrationForm
from app.models import User
from flask_login import logout_user, login_required
from urllib.parse import urlsplit
from datetime import datetime, timezone
from app.forms import EditProfileForm, ResetPasswordForm
from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.user import MyUser
from app.database import Database, CreateClassTable


# NOTE: DUMMY DATA FOR DASHBOARD
headings = ('Database', 'Engine', 'Date Created')


@app.route('/')
@app.route('/index')
@login_required
def index():
    """Handles the index page"""
    db_list = Database(current_user.id).get_fmt_db_dt
    databases = db_list if db_list else [["None", "None", "None"]]
    return render_template('index.html', title='Home',
                           headings=headings, databases=databases)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles the user login page"""
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
    return render_template('login.html', title='Sign In',
                           form=form, current_template='login.html')


@app.route('/logout')
def logout():
    """Handles logout page"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        MyUser(user.id, user.username).addUser()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register',
                           form=form, current_template='register.html')


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    # session['username'] = user
    return render_template('user.html', user=user)


@app.before_request
def before_request():
    """called for every request"""
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Handles profile edit page"""
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
    """password reset request page"""
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
    """handles forgotten password"""
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


@app.route('/upload_database', methods=['GET', 'POST'])
@login_required
def upload_database():
    """Handles the form where sqldump file is uploaded"""
    database_engines = [None, 'MySQL', 'PostgreSQL', 'MariaDB']
    return render_template('database.html', title='Create Database',
                           database_engines=database_engines)


@app.route('/delete_databases', methods=['GET', 'POST'])
@login_required
def delete_dbs():
    """handles deleting of database"""
    if request.method == 'GET':
        db_list = Database(current_user.id).db_list
        if db_list:
            return render_template('database.html',
                                   title='Delete Database', databases=db_list)
        flash("No Database Uploaded Yet")
        return redirect(url_for('index'))
    elif request.method == 'POST':
        selected_dbs = request.form.getlist('dbs')
        Database(current_user.id).del_database(selected_dbs)
        flash("Database(s) Successfully Deleted")
        return redirect(url_for('index'))


@app.route('/submit_database_form', methods=['POST'])
@login_required
def submit_database_form():
    """handles the uploaded sqldump file once it has been uploaded"""
    uploaded_files = request.files.get('uploaded_file')
    filename = request.form.get("filename")
    # db_list = Database(current_user.id).get_fmt_db_dt
    db_list = Database(current_user.id).get_db_list
    for dbs in db_list:
        if filename in dbs:
            print("***** DATABASE ALREADY EXISTED *****")
            Database(current_user.id).del_database(filename)
    db_engine = request.form.get("db_engine")
    db_engine = None if db_engine == "None" else db_engine
    check = MyUser(current_user.id, current_user.username).check_folder(
        uploaded_files, filename, db_engine)
    flash("File Successfully Uploaded") if check else flash(
        "Failed to Upload file; Upload file with right RDB format")
    return redirect(url_for('index'))

@app.route('/landing')
def landing_page():
    return render_template('landing.html')
