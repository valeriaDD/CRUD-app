from flask import Flask, jsonify, request

from cerberus import Validator

from database.users import users
from models.user import User

app = Flask(__name__)

post_request_schema = {
    "name": {"type": 'string', 'required': True},
    "surname": {'type': 'string', 'required': True},
    "age": {'type': 'number', 'required': True},
}

patch_request_schema = {
    'name': {'type': 'string', 'required': False},
    'surname': {'type': 'string', 'required': False},
    'age': {'type': 'integer', 'required': False},
}

post_request_validator = Validator(post_request_schema)
patch_request_validator = Validator(patch_request_schema)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)


@app.route('/users', methods=["POST"])
def add_user():
    data = request.json
    is_data_valid = post_request_validator.validate(data)

    if is_data_valid:
        user = User(data["name"], data["surname"], data["age"])
        user.save()
        return jsonify(user.get()), 201

    return "Invalid data", 400


@app.route('/users/<id>', methods=["PATCH"])
def update_user(id):
    data = request.json
    is_data_valid = patch_request_validator.validate(data)

    if is_data_valid:
        for index in range(len(users)):
            if users[index]["id"] == int(id):
                if "age" in data:
                    users[index]["age"] = data["age"]

                if "name" in data:
                    users[index]["name"] = data["name"]

                if "surname" in data:
                    users[index]["surname"] = data["surname"]

                return '', 204

    return "Invalid data", 400


@app.route('/users/<id>', methods=["GET"])
def get_user(id):
    for index in range(len(users)):
        if users[index]["id"] == int(id):
            return jsonify(users[index])

    return "Not found", 400


@app.route('/users/<id>', methods=["DELETE"])
def delete_user(id):
    for index in range(len(users)):
        if users[index]["id"] == int(id):
            del users[index]
            return '', 200

    return "Not found", 400


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")
