import pytest
from app import app as flask_app
from config.mongodb import mongo

@pytest.fixture
def app():
    #bd en memoria para el test
    flask_app.config['TESTING'] = True
    flask_app.config['MONGO_URI'] = 'mongodb://localhost:27017/test_db'
    
    # reset de la bd antes y después de cada test
    with flask_app.app_context():
        mongo.db.movie.delete_many({})
        mongo.db.users.delete_many({})
    
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
