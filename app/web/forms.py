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
                             'school': data.get('school'),
                             'remark': data.get('remark')})
        instance_list.append(forms)
        for pic in pics:
            instance_list.append(FormImage.create({'id': str(uuid.uuid1()),
                                                   'form_id': forms.id,
                                                   'url': pic}))
        db.session.add_all(instance_list)
    return Success('信息提交成功')


@admin_required
def form_list():
    """后台查看已提交表单"""
    parameter_required(('page_num', 'page_size'))
    forms = Form.query.filter(Form.isdelete == false()
                              ).order_by(Form.createtime.desc()).all_with_page()
    [_fill_form_pics(form) for form in forms]
    return Success('获取成功', data=forms)


def _fill_form_pics(form: "sqlalchemy query object") -> "form sqlalchemy object with pics field":
    form_pics = FormImage.query.filter(FormImage.isdelete == false(),
                                       FormImage.form_id == form.id,
                                       ).all()
    pics = [item['url'] for item in form_pics]
    form.fill('pics', pics)


@admin_required
def delete_form():
    """删除"""
    data = parameter_required('id')
    form = Form.query.filter(Form.isdelete == false(), Form.id == data.get('id')).first_('未找到相关信息')
    with db.auto_commit():
        form.update({'isdelete': True})
        FormImage.query.filter(FormImage.isdelete == false(), FormImage.form_id == form.id).delete_()
        db.session.add(form)
    return Success('删除成功', {'id': form.id})
