from flask import Flask
from flask_restful import Api

from src.database.db import initialize_db
from src.resources.routes import initialize_routes

APP = Flask(__name__)
API = Api(APP)

APP.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movies-ex'
}

initialize_db(APP)
initialize_routes(API)

APP.run()