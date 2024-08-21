from flask import request, Response, jsonify
from config.mongodb import mongo
from bson import json_util, ObjectId
from marshmallow import ValidationError
from schemas.movie_schema import MovieSchema
import logging
from pymongo import errors

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
        logging.error(f"Validation error: {err.messages}")
        return {"errors": err.messages}, 400
    except Exception as e:
        logging.error(f"Unexpected error creating movie: {e}")
        return {"error": "Internal server error"}, 500

def get_movies_service():
    try:
        data = mongo.db.movie.find()
        result = json_util.dumps(data)
        return Response(result, mimetype="application/json")
    except errors.PyMongoError as e:
        # Registra cualquier error relacionado con MongoDB
        logging.error(f"MongoDB error fetching movies: {e}")
        return {"error": "Error retrieving movies from the database"}, 500
    except Exception as e:
        # Captura cualquier otro error general
        logging.error(f"Unexpected error fetching movies: {e}")
        return {"error": "Internal server error"}, 500

def get_movie_service(id):
    try:
        # Validar si el ID es un ObjectId válido
        if not ObjectId.is_valid(id):
            logging.error(f"Invalid ObjectId: {id}")
            return {"error": "Invalid movie ID"}, 400

        # Buscar la película por ID
        data = mongo.db.movie.find_one({'_id': ObjectId(id)})
        
        # Si no se encuentra la película
        if not data:
            logging.warning(f"Movie not found with id: {id}")
            return {"error": "Movie not found"}, 404

        # Convertir el resultado a JSON
        result = json_util.dumps(data)
        return Response(result, mimetype="application/json")
    
    except ValidationError as err:
        logging.error(f"Validation error: {err.messages}")
        return {"errors": err.messages}, 400

    except Exception as e:
        logging.error(f"Unexpected error retrieving movie with id {id}: {e}")
        return {"error": "Internal server error"}, 500

def update_movie_service(id):
    try:
        # Validar si el ID es un ObjectId válido
        if not ObjectId.is_valid(id):
            logging.warning(f"Invalid ObjectId: {id}")
            return jsonify({'error': 'Invalid ID format'}), 400

        data = request.get_json()

        if not data:
            logging.warning(f"Invalid payload, no data provided for movie id {id}")
            return jsonify({'error': 'Invalid payload, no data provided'}), 400

        # Validar solo los campos que se envían en la solicitud
        schema = MovieSchema(partial=True)  # 'partial=True' permite validaciones parciales
        try:
            validated_data = schema.load(data)  # Esto valida los datos basados en el esquema
        except ValidationError as err:
            logging.error(f"Validation error while updating movie id {id}: {err.messages}")
            return jsonify({'errors': err.messages}), 400

        # Realizar la actualización en la base de datos
        response = mongo.db.movie.update_one({'_id': ObjectId(id)}, {'$set': validated_data})

        if response.modified_count >= 1:
            logging.info(f"Movie with id {id} updated successfully")
            return jsonify({'message': 'Movie updated successfully'}), 200
        else:
            logging.warning(f"Movie with id {id} not found or no changes made")
            return jsonify({'error': 'Movie not found or no changes made'}), 404
    except Exception as e:
        logging.error(f"Unexpected error updating movie with id {id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500
   
def delete_movie_service(id):
    try:
        # Validar si el ID es un ObjectId válido
        if not ObjectId.is_valid(id):
            logging.warning(f"Invalid ObjectId: {id}")
            return {"error": "Invalid ID format"}, 400
        
        # Intentar eliminar la película
        response = mongo.db.movie.delete_one({'_id': ObjectId(id)})
        
        if response.deleted_count >= 1:
            logging.info(f"Movie with id {id} deleted successfully")
            return {"message": "Delete successful"}, 200
        else:
            logging.warning(f"Movie with id {id} not found")
            return {"error": "Movie not found"}, 404
    except Exception as e:
        logging.error(f"Unexpected error deleting movie with id {id}: {e}")
        return {"error": "Internal server error"}, 500