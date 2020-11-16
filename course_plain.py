from flask import Flask, jsonify, request, Response
import json

# create an instance of Flask class
app = Flask(__name__) 

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

@app.route('/')
def hello_world():
    return 'Hello world'

@app.route('/courses')
def get_courses():
    return jsonify({'courses': courses})

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

# PUT request need to send all data to update, but PATCH can do partial update
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

# PUT request need to send all data to update, but PATCH can do partial update
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

    
# Run the app in port 5000
app.run(port=5000, host="0.0.0.0") 