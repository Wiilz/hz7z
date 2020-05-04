from ..web.admin import login, create_admin
from ..extensions.base_resource import Resource


class Admin(Resource):
    def post(self, string):
        apis = {
            'login': login,
            'create': create_admin,
        }
        return apis
