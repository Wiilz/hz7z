from ..web.file import upload_img, batch_upload
from ..extensions.base_resource import Resource


class File(Resource):
    def post(self, string):
        apis = {
            'upload': upload_img,
            'batch_upload': batch_upload,
        }
        return apis
