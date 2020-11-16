from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

# binding the instance to a very specific Flask application
db = SQLAlchemy(app)

class User(db.Model): 
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(10), unique=True, nullable=False) 
    password = db.Column(db.String(80), nullable=False) 

    def __repr__(self):
        return str({"user": self.username})
    
    def match_user(username, password):
        user = User.query.filter_by(username=username).filter_by(password=password).first()
        if user is None:
            return False
        return True
    
    def get_all_users():
        return User.query.all()

    def create_user(username, password):
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()