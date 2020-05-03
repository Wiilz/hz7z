from ..web.hello import hello
from ..extensions.base_resource import Resource


class Hello(Resource):
    def get(self, string):
        apis = {
            'get': hello
        }
        return apis
