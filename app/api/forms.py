from ..web.forms import submit_form
from ..extensions.base_resource import Resource


class Forms(Resource):
    def post(self, string):
        apis = {
            'submit': submit_form,
        }
        return apis

    def get(self, string):
        apis = {
        }
        return apis
