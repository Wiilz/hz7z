from ..web.forms import submit_form, form_list, delete_form
from ..extensions.base_resource import Resource


class Forms(Resource):
    def post(self, string):
        apis = {
            'submit': submit_form,
            'delete': delete_form,
        }
        return apis

    def get(self, string):
        apis = {
            'list': form_list,
        }
        return apis
