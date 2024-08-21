from flask import Flask, render_template
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import logging
import os

from config.mongodb import mongo
from routes.movie_routes import movie  
from routes.auth import auth 

#cargar las variables de entorno
load_dotenv()                               
#instancia principal para Flask
app = Flask(__name__)

app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# clave para firmar los JWT
app.config['JWT_SECRET_KEY'] = 'Denilson18.'

# inicializar extensiones
mongo.init_app(app)
jwt = JWTManager(app)

# configurar logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', 
handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])

@app.route('/')
def index(): 
    return render_template('index.html')

# registrar los blueprints/rutas
app.register_blueprint(movie, url_prefix='/movie')
app.register_blueprint(auth, url_prefix='/auth')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
