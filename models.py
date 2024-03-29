from sqla_wrapper import SQLAlchemy
import os


db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))


# db of users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    session_token = db.Column(db.String)


# db of user's data
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    goals = db.Column(db.Integer)
    user_id = db.Column(db.Integer, unique=True)
# foreign key

# GOALS: 1 is maintain, 2 lose 0.5, 3 lose 1, 4 gain 0.5, 5 gain 1
