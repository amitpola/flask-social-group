from .group import GroupApi, GroupsApi, MakeOrRemoveAdmin
from .auth import SignUpApi, LoginApi
from .posts import PostApi

def initialize_routes(api):
    api.add_resource(GroupsApi,'/api/groups')
    api.add_resource(GroupApi,'/api/groups/<id>')

    api.add_resource(MakeOrRemoveAdmin,'/api/groups/<id>/add-or-remove')

    #auth endpoints
    api.add_resource(SignUpApi,'/api/auth/signup')
    api.add_resource(LoginApi,'/api/auth/login')

    #post routes
    api.add_resource(PostApi,'/api/posts')