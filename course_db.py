from flask import Flask, jsonify, request, Response
from courseModel import *
from settings import *
import json

@app.route('/courses')
def get_courses():
    return jsonify({'courses': Course.get_all_courses()})

@app.route('/courses/<string:code>')
def get_course(code):
    result = Course.get_course(code=code)
    return jsonify(result)

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

# PUT request need to send all data to update, but PATCH can do partial update
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

    
# Run the app in port 5000
app.run(port=5000, host="0.0.0.0") 