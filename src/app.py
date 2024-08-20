from flask import Flask, render_template
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os

from config.mongodb import mongo
from routes.movie_routes import movie  # Importa solo todo desde routes.todo
from routes.auth import auth  # Importa auth desde routes.auth

load_dotenv()                                      

app = Flask(__name__)

# Configuración de la URI de MongoDB
app.config['MONGO_URI'] = os.getenv('MONGO_URI')

# Clave secreta para firmar los JWT
app.config['JWT_SECRET_KEY'] = 'supersecretkey'  # Cambia esto a una clave segura

# Inicializar extensiones
mongo.init_app(app)
jwt = JWTManager(app)

@app.route('/')
def index(): 
    return render_template('index.html')

# Registrar los blueprints
app.register_blueprint(movie, url_prefix='/movie')
app.register_blueprint(auth, url_prefix='/auth')  # Registrar el blueprint de auth

if __name__ == '__main__':
    app.run(debug=True)
