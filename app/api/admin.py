from ..web.admin import login, create_admin, update_password, reset_password, get_admin_list, delete_admin
from ..extensions.base_resource import Resource


class Admin(Resource):
    def post(self, string):
        apis = {
            'login': login,
            'create': create_admin,
            'update_password': update_password,
            'reset_password': reset_password,
            'delete': delete_admin,
        }
        return apis

    def get(self, string):
        apis = {
            'list': get_admin_list,
        }
        return apis
