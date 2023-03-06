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

api = Api(app)
bcrypt= Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)

client = Celery(app.name, broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')
client.conf.update(app.config)

app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost/social-group'
}

initialize_db(app)
initialize_routes(api)  

@client.task
def send_mail(data):
    with app.app_context():
        msg = Message("Ping!",
                    sender="admin.ping",
                    recipients=[data['email']])
        msg.body = data['message']
        mail.send(msg)



@app.route('/api/send-mail', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        data = {}
        body = request.get_json()
        
        data['email'] =body.get('email')
        data['first_name'] =body.get('first_name')
        data['last_name'] =body.get('last_name')
        data['message'] =body.get('message')
        duration = int(body.get('duration'))

        send_mail.apply_async(args=[data], countdown=duration)
        flash(f"Email will be sent to {data['email']} in {request.form['duration']}")

        return {'message':'mail sent successfully'},200

if __name__ == '__main__':
    app.run(debug=True)