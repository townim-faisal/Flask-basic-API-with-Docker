from courseModel import db, Course
from userModel import User
from userModel import db as db2

# creating the databse - this file will run only once
db.create_all()

# check the methods for Course Model
Course.add_course(code="CSE115", instructor="John stuart", name="Introduction to programming language")
Course.add_course(code="CSE465", instructor="Andrew ng", name="Introduction toneural network")
print(Course.get_all_courses())
Course.update_course(code="CSE115", instructor="Alvice preisly")
print(Course.get_course(code="CSE115"))

# creating the databse for user
db2.create_all()
# create dummy user
User.create_user(username="faisal", password="faisal")
print(User.get_all_users())