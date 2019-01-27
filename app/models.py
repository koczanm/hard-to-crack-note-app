import random
import time
from datetime import datetime

from passlib.hash import pbkdf2_sha512

from app import db

shared_notes = db.Table('shared_notes',
                        db.Column('note_id', db.Integer,
                                  db.ForeignKey('note.id')),
                        db.Column('user_id', db.Integer,
                                  db.ForeignKey('user.id'))
                        )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    authorized = db.Column(db.Boolean, default=False)
    added_notes = db.relationship('Note', backref='user', lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.hashed_password = pbkdf2_sha512.using(
            rounds=150000, salt_size=15).hash(password)

    def check_password(self, password):
        time.sleep(random.random())
        return pbkdf2_sha512.verify(password, self.hashed_password)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    body = db.Column(db.String(256), nullable=False)
    public = db.Column(db.Boolean, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', secondary=shared_notes, lazy='subquery',
                            backref=db.backref('notes', lazy=True))

    def __init__(self, title, body, public, author_id):
        self.title = title
        self.body = body
        self.public = public
        self.author_id = author_id

    def __repr__(self):
        return '<Note {}>'.format(self.title)
