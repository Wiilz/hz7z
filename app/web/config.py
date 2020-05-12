import uuid

from flask import request
from sqlalchemy import false

from app.config.enums import BannerPosition
from app.extensions.error_response import ParamsError
from app.extensions.interface.user_interface import admin_required
from app.extensions.params_validates import parameter_required
from app.extensions.register_ext import db
from app.extensions.success_response import Success
from app.models import Banner, IndexEntrance


def banner_list():
    """首页banner"""
    args = request.args.to_dict()
    position = args.get('position')
    banner_query = Banner.query.filter(Banner.isdelete == false())
    if position:
        try:
            position = int(position)
            BannerPosition(position)
        except ValueError:
            raise ParamsError('参数错误：position')
        banner_query = banner_query.filter(Banner.position == position)
    banners = banner_query.order_by(Banner.item_order.asc(), Banner.createtime.desc()).all()
    return Success('ok', data=banners)


def index_entrance():
    entraces = IndexEntrance.query.filter(IndexEntrance.isdelete == false()
                                          ).order_by(IndexEntrance.item_order.asc(),
                                                     IndexEntrance.createtime.desc()).all()
    return Success('ok', data=entraces)


@admin_required
def set_banner():
    """添加banner"""
    data = parameter_required(('position', 'img_url', 'item_order'))
    parameter_required({'content_link': '跳转链接'}, datafrom=data)
    try:
        position = int(data.get('position'))
        BannerPosition(position)
    except ValueError:
        raise ParamsError('参数错误：position')
    banner_id = data.get('id')
    banner_dict = {'position': position,
                   'img_url': data.get('img_url'),
                   'content_link': data.get('content_link', ' ').strip(),
                   'item_order': data.get('item_order')}
    with db.auto_commit():
        if not banner_id:
            banner_dict['id'] = str(uuid.uuid1())
            banner = Banner.create(banner_dict)
            msg = '添加成功'
        else:
            banner = Banner.query.filter(Banner.isdelete == false(), Banner.id == banner_id).first_('未找到信息')
            if data.get('delete'):
                banner.update({'isdelete': True})
                msg = '删除成功'
            else:
                banner.update(banner_dict, null='no')
                msg = '更新成功'
        db.session.add(banner)
    return Success(msg, {'id': banner.id})


@admin_required
def set_entrance():
    """编辑首页入口图标"""
    data = parameter_required(('id', 'name', 'img_url', 'content_link', 'item_order'))
    entrance_id = data.get('id')
    entrance_dict = {'img_url': data.get('img_url'),
                     'name': data.get('name'),
                     'content_link': data.get('content_link', ' ').strip(),
                     'item_order': data.get('item_order')}
    entrance = IndexEntrance.query.filter(IndexEntrance.isdelete == false(),
                                          IndexEntrance.id == entrance_id).first_('未找到信息')
    with db.auto_commit():
        entrance.update(entrance_dict)
        db.session.add(entrance)
    return Success('更新成功', {'id': entrance.id})
