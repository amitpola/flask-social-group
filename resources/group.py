from bson import ObjectId
from flask import request,Response
from flask_restful import Resource
from database.models import Group, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import messages
from database.db import social_group_instance
import json
from bson.json_util import dumps

class GroupsApi(Resource):  
    def get(self):  
        collection = social_group_instance.group.find()   
        return Response(dumps(collection),mimetype="application/json",status=200) 
        
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        loggedinUser = User.objects.get(id=user_id)
        user_email = loggedinUser.email

        body = request.get_json()

        group_col_instance = social_group_instance['group']
        group = group_col_instance.insert_one(body)

        document = social_group_instance.group.find_one({"_id":ObjectId(group.inserted_id)})
        if document:
            document['admins'].append(user_email)
            social_group_instance.group.update_one({"_id":document['_id']},{"$set":document})
        return {'id':str(group.inserted_id)}, 200
    
class GroupApi(Resource):
    def get(self,id):
        document = social_group_instance.group.find_one({"_id":ObjectId(id)})
        return Response(dumps(document),mimetype="application/json",status=200)
    
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
        
        document = social_group_instance.group.find_one({"_id":ObjectId(id)})

        if document:
            admins = document['admins']
            moderators = document['moderators']
            members = document['members']

            if admins.count(user_email) != 0:
                if moderators.count(member_to_remove) != 0:
                    moderators.remove(member_to_remove)
                if members.count(member_to_remove) != 0:
                    members.remove(member_to_remove)

            elif moderators.count(user_email) != 0:
                if members.count(member_to_remove) != 0:
                    members.remove(member_to_remove)

            elif members.count(user_email) != 0:
                members.remove(member_to_remove)            
                
        
            social_group_instance.group.update_one({'_id': document['_id']}, {"$set": document})
            return messages.success_message, 200

        return messages.error_message, 401 




        