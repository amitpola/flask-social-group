from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
from datetime import datetime


class SocialPost(db.Document):
    title = db.StringField(required=True,unique=True)
    description = db.StringField(required=True)
    created = db.DateTimeField(default=datetime.utcnow)
    added_by_group = db.ReferenceField('Group')

class Group(db.Document):
    public = db.BooleanField(default=True,required=True)
    name = db.StringField(unique=True,required=True)
    description = db.StringField(unique=True,required=True)
    admins = db.ListField(db.StringField())
    moderators = db.ListField(db.StringField())
    members = db.ListField(db.StringField())
    posts = db.ListField(db.ReferenceField('SocialPost', reverse_delete_rule=db.PULL))
    
Group.register_delete_rule(SocialPost,"added_by_group",db.CASCADE)


class User(db.Document):
    email = db.EmailField(required=True,unique=True)
    password = db.StringField(required=True,min_length=6)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')
    
    def check_password(self,password):
        return check_password_hash(self.password,password)