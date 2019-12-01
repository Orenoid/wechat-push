from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TEXT, text

db = SQLAlchemy()

user_channel = db.Table(
    'user_channel',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channel.id', ondelete='CASCADE'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(30), unique=True)
    create_time = db.Column(db.DateTime, server_default=text('CURRENT_TIMESTAMP'))


class Channel(db.Model):
    __tablename__ = 'channel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', secondary=user_channel,
                            lazy='dynamic', backref=db.backref('channels', lazy='dynamic'))


def transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            db.session.rollback()
            raise

    return wrapper
