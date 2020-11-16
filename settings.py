from flask import Flask

# create an instance of Flask class
app = Flask(__name__) 

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# secret key for JWT
app.config["SECRET_KEY"] = "your.name"