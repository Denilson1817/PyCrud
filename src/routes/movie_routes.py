from flask import Blueprint
from flask_jwt_extended import jwt_required
from services.movie_service import create_movie_service, get_movies_service, get_movie_service, update_movie_service, delete_movie_service

movie = Blueprint('movie',__name__)

@movie.route('/',methods=['GET'])
@jwt_required()
def get_movies():
    return get_movies_service()

@movie.route('/<id>',methods=['GET'])
@jwt_required()
def get_movie(id):
    return get_movie_service(id)

@movie.route('/',methods=['POST'])
@jwt_required()
def create_movie():
    return create_movie_service()

@movie.route('/<id>',methods=['PUT'])
@jwt_required()
def update_movie(id):
    return update_movie_service(id)

@movie.route('/<id>',methods=['DELETE'])
@jwt_required()
def delete_movie(id):
    return delete_movie_service(id)