from .auth import SignupApi, LoginApi
from .movie import MoviesApi, MovieApi


def initialize_routes(api):
    api.add_resource(MoviesApi, '/api/movies')
    api.add_resource(MovieApi, '/api/movies/<id>')
    api.add_resource(SignupApi, '/api/auth/signup')
    api.add_resource(LoginApi, '/api/auth/login')
