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