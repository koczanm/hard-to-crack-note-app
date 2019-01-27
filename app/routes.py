import uuid
from functools import wraps

from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)

from app import app, db
from app.models import Note, User
from app.utils import regex_validate_password, regex_validate_username


def generate_xsrf_token():
    if '_xsrf_token' not in session:
        session['_xsrf_token'] = uuid.uuid4().hex

    return session['_xsrf_token']


def signin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' not in session:
            flash('Not signed in', 'err')
            return redirect(url_for('signin'))

        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()

        if user is None:
            flash('Not signed in', 'err')
            return redirect(url_for('signin'))

        if not user.authorized:
            flash('Not signed in', 'err')
            return redirect(url_for('signin'))

        return f(*args, **kwargs)

    return wrap


@app.before_request
def xsrf_protect():
    if request.method == 'POST':
        token = session.pop('_xsrf_token', None)

        if not token or token != request.form.get('_xsrf_token'):
            abort(403)


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('signin'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not regex_validate_username(username):
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        if not regex_validate_password(password):
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        if not user.check_password(password):
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        user.authorized = True
        db.session.add(user)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        session['user_id'] = user.id
        return redirect(url_for('dashboard'))

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']

        if not regex_validate_username(username):
            flash('Username not allowed', 'err')
            return redirect(url_for('signup'))

        user = User.query.filter_by(username=username).first()

        if user is not None:
            flash('Username taken', 'err')
            return redirect(url_for('signup'))

        if not regex_validate_password(password):
            flash('Password not allowed', 'err')
            return redirect(url_for('signup'))

        if password != password2:
            flash('Different passwords', 'err')
            return redirect(url_for('signup'))

        user = User(username, password)
        db.session.add(user)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        flash('Successfully registered', 'msg')
        return redirect(url_for('signin'))

    return render_template('signup.html')


@app.route('/signout')
def signout():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()
    user.authorized = False
    db.session.add(user)

    try:
        db.session.commit()
    except:
        db.session.rollback()

    session.pop('user_id')

    flash('Successfully signed out', 'msg')
    return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    return 'OK'


@app.route('/dashboard')
def dashboard():
    return 'OK'


@app.route('/notes')
def notes():
    return 'OK'


@app.route('/note/add', methods=['GET', 'POST'])
def add_note():
    return 'OK'


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    return 'OK'
