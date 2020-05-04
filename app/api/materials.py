from ..web.materials import contacts_list, get_contacts, set_contacts
from ..extensions.base_resource import Resource


class Materials(Resource):
    def post(self, string):
        apis = {
            'set_contacts': set_contacts
        }
        return apis

    def get(self, string):
        apis = {
            'contacts_list': contacts_list,
            'contacts': get_contacts,
        }
        return apis
