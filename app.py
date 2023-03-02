from flask import Flask
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

api = Api(app)
bcrypt= Bcrypt(app)
jwt = JWTManager(app)


# def initialize_jwt(app):
#     jwt.init_app(app)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/social-group'
}

initialize_db(app)
initialize_routes(api)  

if __name__ == '__main__':
    app.run(debug=True)