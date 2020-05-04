from ..web.config import banner_list, index_entrance, set_banner, set_entrance
from ..extensions.base_resource import Resource


class Config(Resource):
    def post(self, string):
        apis = {
            'set_banner': set_banner,
            'set_entrance': set_entrance,
        }
        return apis

    def get(self, string):
        apis = {
            'banner_list': banner_list,
            'index_entrance': index_entrance,
        }
        return apis
