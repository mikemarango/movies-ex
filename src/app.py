from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager

from src.database.db import initialize_db
from src.resources.routes import initialize_routes

APP = Flask(__name__)
API = Api(APP)
BCRYPT = Bcrypt(APP)
JWT = JWTManager(APP)

APP.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movies-ex'
}
APP.config.from_envvar('ENV_FILE_LOCATION')

initialize_db(APP)
initialize_routes(API)

APP.run()