"""
create user: wiilz
create time: 2020-05-04
"""
import re
import uuid
from flask import request
from sqlalchemy import false
from ..extensions.token_handler import usid_to_token
from ..extensions.interface.user_interface import admin_required
from ..extensions.params_validates import parameter_required, validate_telephone
from ..extensions.success_response import Success
from ..extensions.error_response import ParamsError, AuthorityError
from ..config.enums import AdminLevel, AdminStatus
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.admin import Admin
from app.extensions.register_ext import db
from ..libs.generate_default_avatar import GithubAvatarGenerator


@admin_required
def create_admin():
    """超级管理员添加普通管理"""
    super_admin = Admin.query.filter(Admin.isdelete == false(),
                                     Admin.id == getattr(request, 'user').id,
                                     Admin.level == AdminLevel.super.value).first()

    if not super_admin:
        return AuthorityError()

    data = parameter_required({'name': '管理员账户名'})
    name, telephone = data.get('name'), data.get('telephone')
    __check_exist_name(name)
    if telephone:
        validate_telephone(telephone)
    with db.auto_commit():
        admin_id = str(uuid.uuid1())
        filedbname, filename = GithubAvatarGenerator().save_avatar(admin_id)
        admin_instance = Admin.create({'id': admin_id,
                                       'name': name,
                                       'telephone': telephone,
                                       'password': generate_password_hash('123456'),
                                       'avatar': filedbname,
                                       'level': AdminLevel.general.value,
                                       'status': AdminStatus.normal.value,
                                       })
        db.session.add(admin_instance)
    return Success('创建管理员成功')


def __check_password(password):
    """
    校检密码
    """
    if not password or len(password) < 4:
        raise ParamsError('密码长度低于4位')
    zh_pattern = re.compile(r'[\u4e00-\u9fa5]+')
    match = zh_pattern.search(password)
    if match:
        raise ParamsError(u'密码中不允许包含中文字符')
    return True


def __check_exist_name(name):
    """账户名校验"""
    exist_name = Admin.query.filter(Admin.isdelete == false(), Admin.name == name).first()
    if exist_name:
        raise ParamsError('用户名已存在')


def login():
    """管理员登录"""
    data = parameter_required({'name': '账户名', 'password': '密码'})
    admin = Admin.query.filter(Admin.isdelete == false(),
                               Admin.name == data.get("name")).first()
    if not admin:
        raise ParamsError('账号不存在')

    if not check_password_hash(admin.password, data.get('password')):
        raise ParamsError('密码不正确')
    token = usid_to_token(admin.id, 'Admin', admin.level, username=admin.name)
    return Success('登录成功', data={'token': token, "admin": admin})


@admin_required
def update_password():
    """更新管理员密码"""
    data = parameter_required(('password_old', 'password_new', 'password_repeat'))

    pwd_new = data.get('password_new')
    pwd_old = data.get('password_old')
    pwd_repeat = data.get('password_repeat')
    if pwd_new != pwd_repeat:
        raise ParamsError('两次输入的密码不相同')
    admin = Admin.query.filter(Admin.isdelete == false(),
                               Admin.status == AdminStatus.normal.value,
                               Admin.id == getattr(request, 'user').id).first_('账号状态异常，请联系超级管理员处理')
    if not check_password_hash(admin.password, pwd_old):
        raise ParamsError('原密码错误')
    with db.auto_commit():
        admin.update({'password': generate_password_hash(pwd_new)})
        db.session.add(admin)
    return Success('密码更新成功')


@admin_required
def reset_password():
    """重置管理员密码"""
    data = parameter_required(('id',))
    # 判断权限
    admin_query = Admin.query.filter(Admin.isdelete == false())
    super_admin = admin_query.filter(Admin.id == getattr(request, 'user').id,
                                     Admin.level == AdminLevel.super.value).first()

    if not super_admin:
        raise AuthorityError()
    admin_id = data.get('id')
    admin = admin_query.filter(Admin.id == admin_id).first_('无此id消息')
    with db.auto_commit():
        admin.update({'password': generate_password_hash('123456')})
        db.session.add(admin)
    return Success('密码重置成功', admin_id)


@admin_required
def delete_admin():
    """删除管理员"""
    data = parameter_required('id')
    # 权限判断
    admin_query = Admin.query.filter(Admin.isdelete == false())
    super_admin = admin_query.filter(Admin.id == getattr(request, 'user').id,
                                     Admin.level == AdminLevel.super.value).first()

    if not super_admin:
        raise AuthorityError()
    admin_id = data.get('id')
    admin = admin_query.filter(Admin.id == admin_id).first_('无此id消息')
    with db.auto_commit():
        admin.update({'isdelete': True})
        db.session.add(admin)
    return Success('账号删除成功', admin_id)


@admin_required
def get_admin_list():
    """管理员列表"""
    parameter_required(('page_num', 'page_size'))
    # 判断权限
    admin_query = Admin.query.filter(Admin.isdelete == false())
    super_admin = admin_query.filter(Admin.id == getattr(request, 'user').id,
                                     Admin.level == AdminLevel.super.value).first()
    if not super_admin:
        raise AuthorityError()
    admin_list = admin_query.order_by(Admin.level.asc(), Admin.createtime.desc()).all_with_page()
    [ad.add('id') for ad in admin_list]
    return Success('获取成功', admin_list)
