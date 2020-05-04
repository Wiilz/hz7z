from ..web.materials import contacts_list, get_contacts, set_contacts, set_material, get_rich_text
from ..extensions.base_resource import Resource


class Materials(Resource):
    def post(self, string):
        apis = {
            'set_contacts': set_contacts,
            'set_material': set_material,
        }
        return apis

    def get(self, string):
        apis = {
            'contacts_list': contacts_list,
            'contacts': get_contacts,
            'rich_text': get_rich_text,
        }
        return apis
