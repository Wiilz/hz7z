from flask import request
from sqlalchemy import false

from app.extensions.success_response import Success
from app.models import Banner, IndexEntrance


def banner_list():
    """首页banner"""
    args = request.args.to_dict()
    position = args.get('position')
    banner_query = Banner.query.filter(Banner.isdelete == false())
    if position:
        banner_query = banner_query.filter(Banner.position == position)
    banners = banner_query.order_by(Banner.item_order.asc(), Banner.createtime.desc()).all()
    return Success('ok', data=banners)


def index_entrance():
    entraces = IndexEntrance.query.filter(IndexEntrance.isdelete == false()
                                          ).order_by(IndexEntrance.item_order.asc(),
                                                     IndexEntrance.createtime.desc()).all()
    return Success('ok', data=entraces)
