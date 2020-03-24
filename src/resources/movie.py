from flask import Response, request
from flask_restful import Resource

from src.database.models import Movie


class MoviesApi(Resource):
    @staticmethod
    def get():
        movies = Movie.objects().to_json()
        return Response(movies, mimetype="application/json", status=200)

    @staticmethod
    def post():
        body = request.get_json()
        movie = Movie(**body).save()
        id = movie.id
        return {'id': str(id)}, 200


class MovieApi(Resource):
    @staticmethod
    def put(id):
        body = request.get_json()
        Movie.objects.get(id=id).update(**body)
        return '', 200

    @staticmethod
    def delete(id):
        Movie.objects.get(id=id).delete()
        return '', 200

    @staticmethod
    def get(id):
        movies = Movie.objects.get(id=id).to_json()
        return Response(movies, mimetype="application/json", status=200)
