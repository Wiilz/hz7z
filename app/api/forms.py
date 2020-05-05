from ..web.forms import submit_form, form_list
from ..extensions.base_resource import Resource


class Forms(Resource):
    def post(self, string):
        apis = {
            'submit': submit_form,
        }
        return apis

    def get(self, string):
        apis = {
            'list': form_list,
        }
        return apis
