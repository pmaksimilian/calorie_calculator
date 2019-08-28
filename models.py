from sqla_wrapper import SQLAlchemy
import os


db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer)
    weight = db.Column(db.Float)
    user_id = db.Column(db.Integer, unique=True)
