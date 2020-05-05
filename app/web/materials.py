import uuid
from flask import request
from sqlalchemy import false
from app.extensions.register_ext import db
from ..extensions.interface.user_interface import admin_required
from ..extensions.params_validates import parameter_required
from ..extensions.success_response import Success
from ..extensions.error_response import ParamsError
from ..models import ContactsCard, MaterialType, RichText, Media


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
def delete_material():
    data = parameter_required(('material_type', 'id'))
    mt = _check_material_type(data.get('material_type'))
    material_id = data.get('id')
    with db.auto_commit():
        if mt.id < 200:
            instance = RichText.query.filter(RichText.isdelete == false(),
                                             RichText.material_type == mt.id,
                                             RichText.id == material_id
                                             ).first_('未找到信息')
            if mt.name not in ('学校官微资讯', '招生简章', '招考信息'):  # 仅可存在一篇
                raise ParamsError('该类型下文章不可删除')
            instance.update({'isdelete': True})
        else:
            instance = Media.query.filter(Media.isdelete == false(),
                                          Media.material_type == mt.id,
                                          Media.id == material_id
                                          ).first_('未找到信息')
            instance.update({'isdelete': True})
        db.session.add(instance)
    return Success('删除成功', {'material_id': material_id})


@admin_required
def set_material():
    data = parameter_required(('material_type',))
    material_type = data.get('material_type')
    mt = _check_material_type(material_type)
    if mt.id < 200:
        return set_rich_text(mt, data)
    else:
        return set_media(mt, data)


def set_media(mt, data):
    """媒体资源/作品展示/校园视频"""
    parameter_required('media_url', datafrom=data)
    base_dict = {'material_type': mt.id, 'media_url': data.get('media_url')}
    if mt.name == '校园视频':  # 240
        parameter_required('cover', datafrom=data)
        if data.get('media_url')[-3:] not in ('mp4', 'avi', 'wmv', 'mov', '3gp', 'flv', 'mpg'):
            raise ParamsError('请检查上传文件格式是否是视频类型')
        base_dict['cover'] = data.get('cover')
    else:
        if data.get('media_url')[-3:] not in ('jpg', 'jpeg', 'png', 'gif'):
            raise ParamsError('请检查上传文件格式是否是图片类型')
    if mt.name != '校园风光':  # !230
        parameter_required({'description': '简介 "description"'}, datafrom=data)
        base_dict['description'] = data.get('description')
    with db.auto_commit():
        if not data.get('id'):
            base_dict['id'] = str(uuid.uuid1())
            base_dict['author_id'] = getattr(request, 'user').id
            media_instance = Media.create(base_dict)
            msg = '添加成功'
        else:
            media_instance = Media.query.filter(Media.isdelete == false(),
                                                Media.material_type == mt.id,
                                                Media.id == data.get('id')).first_('未找到信息')
            media_instance.update(base_dict)
            msg = '更新成功'
        db.session.add(media_instance)
    return Success(msg, {'media_id': media_instance.id})


def set_rich_text(mt, data):
    """编辑富文本文章"""
    parameter_required('content', datafrom=data)
    base_dict = {'material_type': mt.id, 'content': data.get('content')}
    if mt.name in ('招生简章', '招考信息'):  # 30 40
        parameter_required({'title': '标题 "title"'}, datafrom=data)
        base_dict['title'] = data.get('title')
    elif mt.name == '特色教育':  # 60
        parameter_required({'cover': '顶部图片 "cover"'}, datafrom=data)
        base_dict['cover'] = data.get('cover')
    elif mt.name == '学校官微资讯':  # 70
        parameter_required({'title': '标题 "title"', 'cover': '列表页主图 "cover"'}, datafrom=data)
        base_dict['cover'] = data.get('cover')
        base_dict['title'] = data.get('title')
    with db.auto_commit():
        if not data.get('id'):  # 新增
            if mt.name not in ('学校官微资讯', '招生简章', '招考信息'
                               ) and RichText.query.filter(RichText.isdelete == false(),
                                                           RichText.material_type == mt.id
                                                           ).first():  # 仅能存在一篇的类型
                raise ParamsError('该类型重复, 请到已有文章中进行修改')
            if mt.name == '招生简章' and RichText.query.filter(RichText.isdelete == false(),
                                                           RichText.material_type == mt.id,
                                                           RichText.title == data.get('title')):
                raise ParamsError('该标题文章已存在，请检查是否填写重复')
            base_dict['id'] = str(uuid.uuid1())
            base_dict['author_id'] = getattr(request, 'user').id
            rt_instance = RichText.create(base_dict)
            msg = '添加成功'
        else:
            rt_instance = RichText.query.filter(RichText.isdelete == false(),
                                                RichText.id == data.get('id')
                                                ).first_('未找到信息')
            rt_instance.update(base_dict)
            msg = '更新成功'
        db.session.add(rt_instance)
    return Success(msg, data={'rich_text_id': rt_instance.id})


def _check_material_type(material_type):
    mt = MaterialType.query.filter(MaterialType.isdelete == false(),
                                   MaterialType.id == material_type
                                   ).first_('参数错误：material_type，无此分类')
    return mt


def get_rich_text():
    """获取文章内容"""
    args = parameter_required('material_type')
    mt = _check_material_type(args.get('material_type'))
    rich_text_query = RichText.query.filter(RichText.isdelete == false(), )
    if mt.id >= 200:
        raise ParamsError('该 material_type 不属于文章分类')
    if mt.name not in ('学校官微资讯', '招生简章', '招考信息'):  # 仅可存在一篇
        res = rich_text_query.filter(RichText.material_type == mt.id).first_('未找到信息')
    else:
        if args.get('id'):
            res = rich_text_query.filter(RichText.material_type == mt.id,
                                         RichText.id == args.get('id')).first_('未找到信息')
            create_time = str(res.createtime).split('-')
            res.fill('post_time', f"{create_time[0]}年{int(create_time[1])}月{int(create_time[2][:2])}日")

        else:
            res = rich_text_query.filter(RichText.material_type == mt.id
                                         ).order_by(RichText.createtime.desc()).all_with_page()
            for item in res:
                item.hide('content')
                create_time = str(item.createtime).split('-')
                item.fill('post_time', f"{create_time[0]}年{int(create_time[1])}月{int(create_time[2][:2])}日")

    return Success('获取成功', data=res)


def get_medias():
    """获取媒体资源 作品展示/七中视界"""
    args = parameter_required('material_type')
    mt = _check_material_type(args.get('material_type'))
    media_query = Media.query.filter(Media.isdelete == false(), Media.material_type == mt.id)
    if mt.id < 200:
        raise ParamsError('该 material_type 不属于媒体资源分类')
    if args.get('id'):
        res = media_query.filter(Media.id == args.get('id')).first_('未找到信息')
    else:
        res = media_query.order_by(Media.createtime.desc()).all_with_page()
    return Success('获取成功', data=res)
    # if mt.name == '校园视频':
    #     return school_video_list(mt)
    # if args.get('id'):
    #     res = {'previous': {}, 'current': {}, 'next': {}}
    #     current_media = media_query.filter(Media.id == args.get('id')).first_('无此id')
    #     res['current'] = current_media
    #     res['previous'] = (media_query.filter(Media.createtime > current_media.createtime,
    #                                           ).order_by(Media.createtime.asc()).first()
    #                        or media_query.filter(Media.createtime < current_media.createtime
    #                                              ).order_by(Media.createtime.asc()).first()
    #                        or {})  # 寻找当前记录的前一条，当前记录是第一条的时候，返回整个排序最后一条记录
    #     res['next'] = (media_query.filter(Media.createtime < current_media.createtime,
    #                                       ).order_by(Media.createtime.desc()).first()
    #                    or media_query.filter(Media.createtime > current_media.createtime
    #                                          ).order_by(Media.createtime.desc()).first()
    #                    or {})  # 寻找当前记录的后一条，当前记录已经是最后一条的时候，返回整个排序最前一条记录
    # else:
    #     media_instance = media_query.order_by(Media.createtime.desc()).limit(3).all()
    #     res = {'previous': {}, 'current': {}, 'next': {}}
    #     if not media_instance:
    #         res = res
    #     elif len(media_instance) == 1:
    #         res['current'] = media_instance[0]
    #     #  大于一条记录时，即开始循环获取
    #     elif len(media_instance) == 2:
    #         res['current'] = media_instance[0]
    #         res['previous'] = res['next'] = media_instance[1]
    #     else:
    #         res['current'] = media_instance[1]
    #         res['previous'] = media_instance[0]
    #         res['next'] = media_instance[2]

#
# def school_video_list(mt):
#     res = Media.query.filter(Media.isdelete == false(),
#                              Media.material_type == mt.id
#                              ).order_by(Media.createtime.desc()).all_with_page()
#     return Success('获取成功', res)
