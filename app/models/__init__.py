from functools import wraps
from flask_sqlalchemy import SQLAlchemy


def transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            db.session.rollback()
            raise

    return wrapper


db = SQLAlchemy()
