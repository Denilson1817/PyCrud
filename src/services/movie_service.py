from flask import request, Response, jsonify
from config.mongodb import mongo
from bson import json_util, ObjectId
from marshmallow import ValidationError
from schemas.movie_schema import MovieSchema

movie_schema = MovieSchema()

def create_movie_service():
    try:
        data = request.get_json()
        movie_schema.load(data)  # Valida los datos de entrada
        
        name = data.get('name', None)
        actors = data.get('actors', None)
        director = data.get('director', None)
        genre = data.get('genre', None)
        rating = data.get('rating', None)
        realeseDate = data.get('realeseDate', None)
        
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
    except ValidationError as err:
        return {"errors": err.messages}, 400

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
    
    if not data:
        return jsonify({'error': 'Invalid payload, no data provided'}), 400
    
    # Validar solo los campos que se envían en la solicitud
    schema = MovieSchema(partial=True)  # 'partial=True' permite validaciones parciales
    try:
        validated_data = schema.load(data)  # Esto valida los datos basados en el esquema
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400

    # Realizar la actualización en la base de datos
    response = mongo.db.movie.update_one({'_id': ObjectId(id)}, {'$set': validated_data})

    if response.modified_count >= 1:
        return jsonify({'message': 'Movie updated successfully'}), 200
    else:
        return jsonify({'error': 'Movie not found or no changes made'}), 404
   
def delete_movie_service(id):
   response = mongo.db.movie.delete_one({'_id': ObjectId(id)})
   if response.deleted_count >= 1:
      return 'Delete', 200
   else:
      return 'Not Found', 404