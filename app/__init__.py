from flask import Flask
from app.models import Schema, bcrypt, jwt
from flask_cors import CORS
######################################
#### Application Factory Function ####
######################################

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = 'secret'
    return app

