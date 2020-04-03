import datetime

from flask_restful import Resource, request
from flask_jwt_extended import create_access_token
from mongoengine import FieldDoesNotExist, NotUniqueError

from src.database.models import User
from src.resources.errors import SchemaValidationError, EmailAlreadyExistsError, \
    UnauthorizedError, InternalServerError


class SignupApi(Resource):
    @staticmethod
    def post():
        try:
            body = request.get_json()
            user = User(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    @staticmethod
    def post():
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, FieldDoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
