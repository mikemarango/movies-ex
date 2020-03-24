from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from src.database.models import Movie, User


class MoviesApi(Resource):
    @staticmethod
    def get():
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @staticmethod
    @jwt_required
    def post():
        user_id = get_jwt_identity()
        body = request.get_json()
        user = User.objects.get(id=user_id)
        movie = Movie(**body, added_by=user)
        movie.save()
        user.update(push__movies=movie)
        user.save()
        id = movie.id
        return {'id': str(id)}, 200


class MovieApi(Resource):
    @staticmethod
    @jwt_required
    def put(id):
        user_id = get_jwt_identity()
        movie = Movie.objects.get(id=id, added_by=user_id)
        body = request.get_json()
        movie.update(**body)
        return '', 200

    @staticmethod
    @jwt_required
    def delete(id):
        user_id = get_jwt_identity()
        movie = Movie.objects.get(id=id, added_by=user_id)
        movie.delete()
        return '', 200

    @staticmethod
    def get(id):
        movies = Movie.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)
