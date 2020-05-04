import uuid
from flask import request
from sqlalchemy import false
from app.extensions.register_ext import db
from ..extensions.interface.user_interface import admin_required
from ..extensions.params_validates import parameter_required
from ..extensions.success_response import Success
from ..extensions.error_response import ParamsError
from ..models import ContactsCard


def contacts_list():
    """联系我们 列表"""
    con_list = ContactsCard.query.filter(ContactsCard.isdelete == false()
                                         ).order_by(ContactsCard.createtime.desc()).all()
    return con_list


def get_contacts():
    """详情"""
    args = parameter_required('id')
    contact_id = args.get('id')
    contact = ContactsCard.query.filter(ContactsCard.isdelete == false(),
                                        ContactsCard.id == contact_id).first_('未找到信息')
    return contact


@admin_required
def set_contacts():
    """添加/编辑/删除 联系方式"""
    data = request.json or {}
    required_param = ('title', 'address', 'longitude',
                      'latitude', 'telephone', 'fax',
                      'website', 'mailbox', 'headmaster')
    contacts_id = data.get('id')
    longitude, latitude = data.get('longitude'), data.get('latitude')
    contact_dict = {'title': data.get('title'), 'address': data.get('address'),
                    'telephone': data.get('telephone'), 'fax': data.get('fax'),
                    'website': data.get('website'), 'mailbox': data.get('mailbox'),
                    'headmaster': data.get('headmaster')}

    with db.auto_commit():
        if not contacts_id:
            parameter_required(required_param, datafrom=data)
            latitude, longitude = _check_lat_and_long(latitude, longitude)
            contact_dict['latitude'] = latitude
            contact_dict['longitude'] = longitude
            contact_dict['id'] = str(uuid.uuid1())
            contacts = ContactsCard.create(contact_dict)
            msg = '添加成功'
        else:
            contacts = ContactsCard.query.filter(ContactsCard.isdelete == false(),
                                                 ContactsCard.id == contacts_id).first_('未找到信息')
            if data.get('delete'):
                contacts.update({'isdelete': True})
                msg = '删除成功'
            else:
                parameter_required(required_param, datafrom=data)
                latitude, longitude = _check_lat_and_long(latitude, longitude)
                contact_dict['latitude'] = latitude
                contact_dict['longitude'] = longitude
                contacts.update(contact_dict)
                msg = '更新成功'
        db.session.add(contacts)
    return Success(msg, {'contacts_id': contacts.id})


def _check_lat_and_long(lat, long):
    try:
        if not -90 <= float(lat) <= 90:
            raise ParamsError('纬度错误，范围 -90 ~ 90')
        if not -180 <= float(long) <= 180:
            raise ParamsError('经度错误，范围 -180 ~ 180')
    except (TypeError, ValueError):
        raise ParamsError('经纬度应为合适范围内的浮点数')
    return str(lat), str(long)


@admin_required
def set_material():
    data = parameter_required(('material_type', 'content'))
    material_type, title, content = map(lambda x: data.get(x), ('material_type', 'title', 'content'))
