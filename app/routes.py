from datetime import datetime, timedelta
from functools import wraps

from flask import (abort, flash, redirect, render_template, request, session,
                   url_for)

from app import app, db
from app.models import Note, User
from app.utils import validate_username, validate_password, validate_title, valitdate_body


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
def before_request():
    if not request.is_secure:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)


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
        username = request.form.get('username')
        password = request.form.get('password')

        if not validate_username(username):
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        if not validate_password(password):
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        user = User.query.filter_by(username=username).first()

        if user is None:
            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        if user.date_blocking > datetime.utcnow():
            flash('Temporarily blocked')
            return redirect(url_for('signin'))

        if not user.check_password(password):
            user.bad_attempts += 1

            print(user.bad_attempts)

            if user.bad_attempts == 5:
                user.bad_attempts = 0
                user.date_blocking = datetime.utcnow() + timedelta(minutes=5)

                db.session.add(user)

                try:
                    db.session.commit()
                except:
                    db.session.rollback()

            flash('Invalid username or password', 'err')
            return redirect(url_for('signin'))

        user.authorized = True
        user.bad_attempts = 0
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
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if not validate_username(username):
            flash('Username not allowed', 'err')
            return redirect(url_for('signup'))

        user = User.query.filter_by(username=username).first()

        if user is not None:
            flash('Username taken', 'err')
            return redirect(url_for('signup'))

        if not validate_password(password):
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
@signin_required
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
@signin_required
def account():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).first()

        if not validate_password(current_password):
            flash('Invalid password', 'err')
            return redirect(url_for('account'))

        if not user.check_password(current_password):
            flash('Invalid password', 'err')
            return redirect(url_for('account'))

        if not validate_password(password):
            flash('Password not allowed', 'err')
            return redirect(url_for('account'))

        if password != password2:
            flash('Different passwords', 'err')
            return redirect(url_for('account'))

        user.set_password(password)
        db.session.add(user)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        flash('Successfully changed', 'msg')
        return redirect(url_for('account'))

    return render_template('account.html')


@app.route('/dashboard')
@signin_required
def dashboard():
    user_id = session['user_id']
    pub_notes = Note.query.filter_by(public=True).all()
    priv_notes = Note.query.filter_by(public=False).join(
        Note.users).filter_by(id=user_id).all()

    return render_template('dashboard.html', pub_notes=pub_notes, priv_notes=priv_notes)


@app.route('/notes')
@signin_required
def notes():
    user_id = session['user_id']
    user_notes = Note.query.filter_by(author_id=user_id).all()

    return render_template('note/list.html', notes=user_notes)


@app.route('/note/add', methods=['GET', 'POST'])
@signin_required
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        if not validate_title(title):
            flash('Invalid data', 'err')
            return redirect(url_for('add_note'))

        if not valitdate_body(body):
            flash('Invalid data', 'err')
            return redirect(url_for('add_note'))

        if 'public' in request.form:
            public = True
        else:
            public = False

        author_id = session['user_id']
        author = User.query.filter_by(id=author_id).first()
        users = request.form.getlist('user')

        note = Note(title, body, public, author_id)
        note.users.append(author)

        for username in users:
            if validate_username(username):
                user = User.query.filter_by(username=username).first()

                if user is not None:
                    note.users.append(user)

        db.session.add(note)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('dashboard'))

    return render_template('note/add.html')


@app.route('/note/<int:note_id>', methods=['GET', 'POST'])
@signin_required
def edit_note(note_id):
    author_id = session['user_id']
    author = User.query.filter_by(id=author_id).first()
    note = Note.query.filter_by(id=note_id).filter_by(
        author_id=author_id).first()

    if note is None:
        return render_template('note/edit.html')

    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        if not validate_title(title):
            flash('Invalid data', 'err')
            return redirect(url_for('add_note'))

        if not valitdate_body(body):
            flash('Invalid data', 'err')
            return redirect(url_for('add_note'))

        if 'public' in request.form:
            public = True
        else:
            public = False

        users = request.form.getlist('user')

        edited_note = Note(title, body, public, author_id)
        edited_note.users.append(author)

        for username in users:
            if validate_username(username):
                user = User.query.filter_by(username=username).first()

                if user is not None:
                    edited_note.users.append(user)

        db.session.delete(note)
        db.session.add(edited_note)

        try:
            db.session.commit()
        except:
            db.session.rollback()

        return redirect(url_for('notes'))

    users = note.users
    users.remove(author)

    return render_template('note/edit.html', note=note, users=users)
