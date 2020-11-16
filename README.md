# Flask with Docker and JWT

## Getting started

Flask is just the barebone, not like other full stake web development framework i.e. django, laravel, ruby on rails etc. Flask is best for building APIs, prototyping code before starting development, using as a sandbox development environment.



1. Download python latest version from [here](https://www.python.org/downloads/)and install pip from [here](https://pip.pypa.io/en/stable/installing/). 

1. Use pipenv by running `pip install pipenv`. You can learn the basic usage of pipenv from [here](https://pipenv-fork.readthedocs.io/en/latest/basics.html). 

1. Install flask by running `pipenv install flask`.

1. Activate the pipenv by running` pipenv shell`.

1. Download postman from [here](https://www.postman.com/downloads/)to check the apis.



## CRUD Data

You can quick start by following this [link](https://flask.palletsprojects.com/en/1.1.x/quickstart/). Also, you will find a tutorial [here](https://flask.palletsprojects.com/en/1.1.x/tutorial/).



Create a course_plain.py file  and put the codes below in there.

```
from flask import Flask, jsonify, request, Response
import json
```


Create an instance of Flask class.

```
app = Flask(__name__) 
```


Create a basic `course` list 

```
courses = [
    {
        'name': 'Introduction to neural network',
        'code': 'CSE465',
        'instructor': 'Andrew Ng'
    },
    {
        'name': 'Introduction to programming language',
        'code': 'CSE115',
        'instructor': 'John stuart'
    },
]
```


Create `get_courses` function for the GET method to retrieve all courses. Here, `app.route` decorator needs parameter for url link. `jsonify` will serialize the data to json object.

```
@app.route('/courses')
def get_courses():
    return jsonify({'courses': courses})
```


You can get a single course also. Here, we pass an argument in the link.

```
@app.route('/courses/<string:code>')
def get_course(code):
    result = {}
    for course in courses:
        if course['code']==code:
            result = {
                "name": course["name"],
                "instructor": course["instructor"]
            }
            break
    return jsonify(result)
```


You can create a request using POST method. Here, we validate the data by check the `code` key is provided. Here, `Response` will give status code 201 when it successfully create a new course. It will show an error message with status code 400 when the validation is failed.

```
@app.route('/courses', methods=['POST'])
def post_course():
    data = request.get_json()
    # validate the data
    if(data["code"] != ""):
        courses.insert(0, {
            "name": data["name"],
            "code": data["code"],
            "instructor": data["instructor"]
        })
        response = Response("", status=201, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(data["code"])
    else:
        error_message = {
            "error": "course code must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


We can do PUT request by sending all data to update a single course’s all value. The responses are same.

```
@app.route('/courses/<string:code>', methods=['PUT'])
def put_course(code):
    data = request.get_json()
    if("instructor" in data and "name" in data):
        for course in courses:
            if course["code"]==code:
                course["instructor"] = data["instructor"]
                course["name"] = data["name"]
                break
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(code)
    else:
        error_message = {
            "error": "Course name and instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


Also, for partial update, we can use PATCH method. The responses are same.

```
@app.route('/courses/<string:code>', methods=['PATCH'])
def patch_course(code):
    data = request.get_json()
    if("instructor" in data or "name" in data):
        for course in courses:
            if course["code"]==code:
                if("instructor" in data):
                    course["instructor"] = data["instructor"]
                if("name" in data):
                    course["name"] = data["name"]
                break
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(code)
    else:
        error_message = {
            "error": "Course name or instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


Delete a course, we can use DELETE method in the decorator. The responses are same.

```
@app.route('/courses/<string:code>', methods=['DELETE'])
def delete_course(code):
    for course in courses:
        if course["code"]==code:
            courses.remove(course)
            response = Response("", status=204, mimetype="application/json")
            response.headers["Location"] = "/courses/"
            return response
    # if course is not found
    error_message = {
        "error": "Course code is not found in the courses"
    }
    response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


To run the app in port 5000, add these codes.

```
app.run(port=5000, host="0.0.0.0") 
```




Now, run `python course_plain.py` in command prompt. It will tell you to go to http://127.0.0.1:5000/. Open postman and you will check each function with their provided request method and url. Below is the example for creating new course.
[Image: image]

## CRUD Data through database

For ORM, you can run `pipenv install Flask-SQLAlchemy`. You can read the documentation [here](https://flask-sqlalchemy.palletsprojects.com/en/2.x/#requirements). You can follow [this quickstart](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application) to learn more about Flask SQLAlchemy.



Create a settings.py file and add these codes.

```
from flask import Flask

# create an instance of Flask class
app = Flask(__name__) 

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:/T.Faisal/example-flask/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
```




Create a courseModel.py and add these codes. `Course` object represents the course table

```
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
        
```


Create create_database.py and add following codes.

```
from courseModel import db, Course
# creating the databse - this file will run only once
db.create_all()
# check the methods for Course Model
Course.add_course(code="CSE115", instructor="John stuart", name="Introduction to programming language")
Course.add_course(code="CSE465", instructor="Andrew ng", name="Introduction toneural network")
print(Course.get_all_courses())
Course.update_course(code="CSE115", instructor="Alvice preisly")
print(Course.get_course(code="CSE115"))
```


Run `python create_database.py` in command prompt. It will create a database and add dummy data there.

You can view the database’s sql code just by running `cat database.db` in command prompt.



Create a file named course_db.py and add below codes.

```
from flask import Flask, jsonify, request, Response
from courseModel import *
from settings import *
import json
```


Create `get_courses` function for the GET method to retrieve all courses.

```
@app.route('/courses')
def get_courses():
    return jsonify({'courses': Course.get_all_courses()})
```


Create `get_course` function to retrieve a single course by course code.

```
@app.route('/courses/<string:code>')
def get_course(code):
    result = Course.get_course(code=code)
    return jsonify(result)
```


Create `post_course` method to insert a new course in database.

```
@app.route('/courses', methods=['POST'])
def post_course():
    data = request.get_json()
    # validate the data
    if(data["code"] != ""):
        Course.add_course(code=data["code"],instructor=data["instructor"],name=data["name"])
        response = Response("", status=201, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(data["code"])
    else:
        error_message = {
            "error": "course code must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


Method for deleting course isbelow.

```
@app.route('/courses/<string:code>', methods=['DELETE'])
def delete_course(code):
    if(Course.delete_course(code=code)):
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"
        return response
    # if course is not found
    error_message = {
        "error": "Course code is not found in the courses"
    }
    response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response
```


Method for update course is below.

```
# PUT request need to send all data to update, but PATCH can do partial update
@app.route('/courses/<string:code>', methods=['PUT'])
def put_course(code):
    data = request.get_json()
    if("instructor" in data and "name" in data):
        Course.update_course(code=code,instructor=data["instructor"],name=data["name"])
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(code)
    else:
        error_message = {
            "error": "Course name and instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response

@app.route('/courses/<string:code>', methods=['PATCH'])
def patch_course(code):
    data = request.get_json()
    if("instructor" in data):
        Course.update_course(code=code,instructor=data["instructor"])
    elif("name" in data):
        Course.update_course(code=code,name=data["name"])
    else:
        error_message = {
            "error": "Course name or instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
        return response
    response = Response("", status=204, mimetype="application/json")
    response.headers["Location"] = "/courses/"+str(code)
    return response
```


To run the app in port 5000, add these codes.

```
app.run(port=5000) 
```


Now, run `python course_plain.py` in command prompt.



## Authentication using JWT

You can use PyJWT from [here](https://pyjwt.readthedocs.io/en/stable/index.html), or you can use Flask-JWT from [here](https://pythonhosted.org/Flask-JWT/). Here, we have used PyJWT. To install pyJWT, run `pipenv install pyjwt` in the command prompt and then activate pipenv.



Here, we show basic authentication system. But to need more secure authentication, we can use Flask-security package from [here](https://pythonhosted.org/Flask-Security).


Put following line of code in settings.py

```
# secret key for JWT
app.config["SECRET_KEY"] = "your.name"
```

Create a userModel.py and add these codes for User database. Here, `match_user` will match the username and password.

```
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
```

Run these lines from command prompt to crate a dummy user:

```
python
from userModel import *
# creating the databse - this file will run only once
db.create_all()
# create dummy user
User.create_user(username="faisal", password="faisal")
print(User.get_all_users())
```

Now, create a file named course_db_authenticate.py and put following codes:

```
from flask import Flask, jsonify, request, Response
from functools import wraps
from courseModel import *
from userModel import *
from settings import *
import json
import jwt
import datetime

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = str(data["username"])
    password = str(data["password"])
    match = User.match_user(username=username, password=password)
    if match:
        expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=200)
        token = jwt.encode({'exp': expiration_date}, app.config["SECRET_KEY"], algorithm="HS256")
        return token
    error_message = {
        "error": "username or password is not correct"
    }
    return Response(json.dumps(error_message), status=400, mimetype="application/json")
    

# decorator for verifying the JWT 
def token_required(f): 
    @wraps(f)
    def decorated(*args, **kwargs): 
        token = request.args.get("token")
        try:
            jwt.decode(token, app.config["SECRET_KEY"])
            return f(*args, **kwargs)
        except:
            return jsonify({'eroor': "Invalid token"})
    return decorated
   

@app.route('/courses')
@token_required
def get_courses():
    return jsonify({'courses': Course.get_all_courses()})

@app.route('/courses/<string:code>')
@token_required
def get_course(code):
    result = Course.get_course(code=code)
    return jsonify(result)

@app.route('/courses', methods=['POST'])
@token_required
def post_course():
    data = request.get_json()
    # validate the data
    if(data["code"] != ""):
        Course.add_course(code=data["code"],instructor=data["instructor"],name=data["name"])
        response = Response("", status=201, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(data["code"])
    else:
        error_message = {
            "error": "course code must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response

# PUT request need to send all data to update, but PATCH can do partial update
@app.route('/courses/<string:code>', methods=['PUT'])
@token_required
def put_course(code):
    data = request.get_json()
    if("instructor" in data and "name" in data):
        Course.update_course(code=code,instructor=data["instructor"],name=data["name"])
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"+str(code)
    else:
        error_message = {
            "error": "Course name and instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response

# PUT request need to send all data to update, but PATCH can do partial update
@app.route('/courses/<string:code>', methods=['PATCH'])
@token_required
def patch_course(code):
    data = request.get_json()
    if("instructor" in data):
        Course.update_course(code=code,instructor=data["instructor"])
    elif("name" in data):
        Course.update_course(code=code,name=data["name"])
    else:
        error_message = {
            "error": "Course name or instructor's name must be provided"
        }
        response = Response(json.dumps(error_message), status=400, mimetype="application/json")
        return response
    response = Response("", status=204, mimetype="application/json")
    response.headers["Location"] = "/courses/"+str(code)
    return response

@app.route('/courses/<string:code>', methods=['DELETE'])
@token_required
def delete_course(code):
    if(Course.delete_course(code=code)):
        response = Response("", status=204, mimetype="application/json")
        response.headers["Location"] = "/courses/"
        return response
    # if course is not found
    error_message = {
        "error": "Course code is not found in the courses"
    }
    response = Response(json.dumps(error_message), status=400, mimetype="application/json")
    return response

    
# Run the app in port 5000
app.run(port=5000) 
```

The `login` method creates a token for valid user. The `token_required` is a wrapper function for all other protected routes, so this method pass to other methods.
Get the token 
[Image: Capture.JPG]
## Dockeraize the project

You can follow this example from [here](https://github.com/fdhadzh/flask-pipenv-example).



Create a DOCKERFILE either through [visual studio’s Docker extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) or by manually put the following codes in file.

```
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app
# Install pipenv requirements
RUN pip3 install -r requirements.txt

EXPOSE 5000
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "course_db.py"]
```


Run following command to build the image.

```
docker build -t flask-course:1.0 .
```


Run the container for created docker image.

```
docker run --publish 5000:5000 --detach --name flaskcourseapi flask-course:1.0
```

To get the IP of the docker container, run command:

```
docker inspect -f 'range .NetworkSettings.Networks.IPAddressend' flaskcourseapi
```


You will get full project link [here](https://github.com/townim-faisal/Flask-basic-API-with-Docker) in github.

## Furthur Analysis

* Flask RESRful [[link](https://flask-restful.readthedocs.io/en/latest/)]
* Flask-JWT-extended [[link](https://flask-jwt-extended.readthedocs.io/en/stable/)]

