import uuid
from flask import request
from sqlalchemy import false
from app.extensions.register_ext import db
from ..extensions.interface.user_interface import admin_required
from ..extensions.params_validates import parameter_required, validate_telephone
from ..extensions.success_response import Success
from ..extensions.error_response import ParamsError
from ..models import Form, FormImage


def submit_form():
    data = parameter_required({'name': '姓名', 'telephone': '电话', 'school': '学校'})
    telephone = data.get('telephone')
    validate_telephone(telephone)
    pics = data.get('pics') or ()
    if pics and not isinstance(pics, list):
        raise ParamsError('参数格式错误: pics')
    instance_list = []
    with db.auto_commit():
        forms = Form.create({'id': str(uuid.uuid1()),
                             'name': data.get('name'),
                             'telephone': telephone,
                             'school': data.get('school')})
        instance_list.append(forms)
        for pic in pics:
            instance_list.append(FormImage.create({'id': str(uuid.uuid1()),
                                                   'form_id': forms.id,
                                                   'url': pic}))
        db.session.add_all(instance_list)
    return Success('信息提交成功')
