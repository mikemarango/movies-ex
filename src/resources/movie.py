from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, \
    ValidationError, InvalidQueryError
from src.resources.errors import SchemaValidationError, MovieAlreadyExistsError, \
    InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError

from src.database.models import Movie, User


class MoviesApi(Resource):
    @staticmethod
    def get():
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @staticmethod
    @jwt_required
    def post():
        try:
            user_id = get_jwt_identity()
            body = request.get_json()
            user = User.objects.get(id=user_id)
            movie = Movie(**body, added_by=user)
            movie.save()
            user.update(push__movies=movie)
            user.save()
            id = movie.id
            return {'id': str(id)}, 200
        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError
        except NotUniqueError:
            raise MovieAlreadyExistsError
        except Exception:
            raise InternalServerError


class MovieApi(Resource):
    @staticmethod
    @jwt_required
    def put(id):
        try:
            user_id = get_jwt_identity()
            movie = Movie.objects.get(id=id, added_by=user_id)
            body = request.get_json()
            movie.update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @staticmethod
    @jwt_required
    def delete(id):
        try:
            user_id = get_jwt_identity()
            movie = Movie.objects.get(id=id, added_by=user_id)
            movie.delete()
            return '', 200
        except DoesNotExist:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    @staticmethod
    def get(id):
        try:
            movies = Movie.objects.get(id=id).to_json()
            return Response(movies, mimetype="application/json", status=200)
        except DoesNotExist:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError
