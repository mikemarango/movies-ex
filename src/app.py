from flask import Flask, Response, request


from src.database.models import Movie
from src.database.db import initialize_db

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/movies-ex'
}

db = initialize_db(app)


@app.route('/movies')
def get_movies():
    movies = Movie.objects.to_json()
    return Response(movies, mimetype='application/json', status=200)


@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    movie = Movie(**body).save()
    id = movie.id
    return {'id': str(id)}, 200


@app.route('/movies/<id>', methods=['PUT'])
def update_movie(id):
    body = request.get_json()
    Movie.objects.get(id=id).update(**body)
    return '', 200


@app.route('/movies/<id>', methods=['DELETE'])
def delete_movie(id):
    Movie.objects.get(id=id).delete()
    return '', 200


@app.route('/movies/<id>', methods=['GET'])
def get_movie(id):
    movies = Movie.objects.get(id=id).to_json()
    return Response(movies, mimetype='application/json', status=200)


app.run()