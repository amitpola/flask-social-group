from flask import Flask, flash, render_template, request, redirect, url_for
from database.db import initialize_db
from flask_restful import Api
from resources.routes import initialize_routes
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from celery import Celery

load_dotenv()

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
app.config['MAIL_DEFAULT_SENDER'] = 'infinity.pola000@gmail.com'

api = Api(app)
bcrypt= Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

client = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
client.conf.update(app.config)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/social-group'
}

initialize_db(app)
initialize_routes(api)  

@client.task
def send_mail(data):
    with app.app_context():
        print(data)
        msg = Message("Welcome to social group!", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[data['email']])
        msg.body = data['message']
        mail.send(msg)

@app.route('/', methods=['POST'])
def index():
    if request.method == 'POST':
        
        data = {}
        body = request.get_json()
        
        data['email'] =body.get('email')
        data['message'] =body.get('message')
        print([data])

        send_mail.apply_async(args=[data], countdown=5)
        flash(f"Email will be sent to {data['email']} 5 seconds")

        return {'message':'mail sent successfully'},200

if __name__ == '__main__':
    app.run(debug=True)