# -*- coding: utf-8 -*-
"""
create user: wiilz
create time:2020-05-04
"""

from sqlalchemy import String, Text, Integer
from ..extensions.base_model import Base, Column


class Banner(Base):
    """首页banner"""
    __tablename__ = 'Banner'
    id = Column(String(64), primary_key=True)
    position = Column(Integer, default=1, comment='位置 1：顶部 2：中间')
    img_url = Column(Text, url=True, comment='图片')
    content_link = Column(Text, comment='链接内容')
    item_order = Column(Integer, default=0, comment='图标顺序')


class IndexEntrance(Base):
    """首页中部自定义图标"""
    __tablename__ = 'IndexEntrance'
    id = Column(String(64), primary_key=True)
    img_url = Column(Text, url=True, comment='图标')
    content_link = Column(Text, comment='链接内容')
    name = Column(String(64), comment='图标名称')
    item_order = Column(Integer, default=0, comment='图标顺序')
