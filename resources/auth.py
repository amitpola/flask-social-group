from database.models import User
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
import datetime

class SignUpApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        return {'message':'User Signed in','id':str(user.id)}, 200
    
class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.objects.get(email=body.get('email'))
        authorized = user.check_password(body.get('password'))

        if not authorized:
            return {'error message':'email or password is incorrect'}, 401
        
        access_token = create_access_token(identity=str(user.id),expires_delta=datetime.timedelta(days=2))
        return {'token':access_token},200