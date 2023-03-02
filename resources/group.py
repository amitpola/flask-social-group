from flask import request,Response
from flask_restful import Resource
from database.models import Group, User
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from utils import messages

class GroupsApi(Resource):  
    def get(self):  
        groups = Group.objects().to_json()
        return Response(groups,mimetype="application/json",status=200)
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = loggedinUser.email
        body = request.get_json()
        group = Group(**body)
        group.admins.append(str(user_email))
        group.save()
        return {'id':str(group.id)}, 200
    
class GroupApi(Resource):
    def get(self,id):
        group = Group.objects.get(id=id).to_json()
        return Response(group,mimetype="application/json",status=200)
    
    @jwt_required()
    def put(self,id):        
        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = str(loggedinUser.email)
        group = Group.objects.get(id=id)

        if group.admins.count(user_email) != 0:
            body = request.get_json()
            Group.objects.get(id=id).update(**body)
            return messages.success_message,200
        
        return messages.error_message, 401
    
    @jwt_required()
    def delete(self,id):
        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = str(loggedinUser.email)
        group = Group.objects.get(id=id)
        
        if group.admins.count(user_email) != 0:
            Group.objects.get(id=id).delete()
            return messages.success_message, 200
        
        return messages.error_message, 401
    
class MakeOrRemoveAdmin(Resource):
    @jwt_required()
    def post(self,id):
        body = request.get_json()
        admin_to_make = body['email']

        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = str(loggedinUser.email)
        group = Group.objects.get(id=id)

        if group.admins.count(user_email) != 0:
            group.admins.append(str(admin_to_make))
            group.save()
            return messages.success_message, 200
        
        return messages.error_message, 401

    @jwt_required()
    def delete(self,id):
        body = request.get_json()
        member_to_remove = body['email']

        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = str(loggedinUser.email)
        group = Group.objects.get(id=id)

        if group.admins.count(user_email) != 0:
            if group.admins.count(member_to_remove) != 0:
                group.admins.remove(member_to_remove)
            elif group.moderators.count(member_to_remove) != 0:
                group.moderators.remove(member_to_remove)
            elif group.members.count(member_to_remove) != 0:
                group.members.remove(member_to_remove)
            
            group.save()
            
            return messages.success_message, 200
        
        return messages.error_message, 401 




        