from flask_mongoengine import MongoEngine
from pymongo import MongoClient

client = MongoClient('mongodb://localhost/social-group')

social_group_instance = client['social-group']

db = MongoEngine()

def initialize_db(app):
    db.init_app(app)