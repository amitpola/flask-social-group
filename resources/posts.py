from database.models import SocialPost
from flask import request, Response
from flask_restful import Resource

class PostApi(Resource):
    def get(self):
        posts = SocialPost.objects().to_json()
        return Response(posts,mimetype="application/json",status=200)

    def post(self):
        body = request.get_json()
        post = SocialPost(**body).save()
        return {'id':str(post.id)}, 200