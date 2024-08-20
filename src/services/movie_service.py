from flask import request, Response
from config.mongodb import mongo
from bson import json_util, ObjectId


def create_movie_service():
    data = request.get_json()
    name = data.get('name', None)
    actors = data.get('actors', None)
    director = data.get('director',None)
    genre  = data.get('genre',None)
    rating = data.get('rating',None)
    realeseDate = data.get('realeseDate',None)
    if name:
      response = mongo.db.movie.insert_one({
        'name': name,
        'actors': actors,
        'director': director,
        'genre': genre,
        'rating': rating,
        'realeseDate': realeseDate,
        'done': False
      })
      result = {
        'id': str(response.inserted_id),
        'name': name,
        'actors': actors,
        'director': director,
        'genre': genre,
        'rating': rating,
        'realeseDate': realeseDate,
        'done': False
      }
      return result
    else:
      return 'Invalid payload', 400

def get_movies_service():
   data=mongo.db.movie.find()
   result = json_util.dumps(data)
   return Response(result, mimetype="application/json")
#Detalle estetico, para pasar el resultado en un formato json adecuado

def get_movie_service(id):
   data = mongo.db.movie.find_one({'_id': ObjectId(id)})
   result = json_util.dumps(data)
   return Response(result, mimetype="application/json")

def update_movie_service(id):
   data = request.get_json()
   if len(data) == 0 :
      return 'invalid payload', 400
   
   response = mongo.db.movie.update_one({'_id': ObjectId(id)},{'$set':data})
   if response.modified_count >= 1: 
      return 'update', 200
   else: 
      return 'Not found', 404
   
def delete_movie_service(id):
   response = mongo.db.movie.delete_one({'_id': ObjectId(id)})
   if response.deleted_count >= 1:
      return 'Delete', 200
   else:
      return 'Not Found', 404