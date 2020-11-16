from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

# binding the instance to a very specific Flask application
db = SQLAlchemy(app)

class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), unique=True, nullable=False)
    instructor = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        course = {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'instructor': self.instructor
        }
        return json.dumps(course)
    
    # to convert a json object
    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'instructor': self.instructor
        }

    def add_course(code, instructor, name):
        new_course = Course(code=code, instructor=instructor, name=name)
        db.session.add(new_course)
        db.session.commit()
    
    def get_all_courses():
        return [Course.json(course) for course in Course.query.all()]

    def get_course(code):
        return Course.json(Course.query.filter_by(code=code).first())

    def delete_course(code):
        success = Course.query.filter_by(code=code).delete()
        db.session.commit()
        return bool(success)
    
    def update_course(code, instructor=None, name=None):
        course = Course.query.filter_by(code=code).first()
        if instructor is not None:
            course.instructor = instructor
        if name is not None:
            course.name = name
        db.session.commit()
        