from flask import Flask, request, jsonify
from service import ToDoService, UserService
from models import Schema, bcrypt, jwt
from flask_cors import CORS

import json

app = Flask(__name__)
bcrypt.init_app(app)
jwt.init_app(app)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'secret'


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/<name>")
def hello_name(name):
    return "Hello " + name


@app.route("/todo/get", methods=["POST"])
def list_todo():
    return jsonify(ToDoService().list(request.get_json()))


@app.route("/todo/create", methods=["POST"])
def create_todo():
    return jsonify(ToDoService().create(request.get_json()))


@app.route("/todo/<item_id>", methods=["PUT"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))


@app.route("/todo/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    return jsonify(ToDoService().delete(item_id))


@app.route('/users/register', methods=['POST'])
def register():
    return jsonify(UserService().create(request.get_json()))


@app.route('/users/login', methods=['POST'])
def login():
    return jsonify(UserService().login(request.get_json()))


if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0')
