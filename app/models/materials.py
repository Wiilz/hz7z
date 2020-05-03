# -*- coding: utf-8 -*-
"""
create user: wiilz
create time: 2020-05-04
"""
from ..extensions.base_model import Base, Column
from sqlalchemy import Integer, String, Text, orm, false
from sqlalchemy.dialects.mysql import LONGTEXT


class RichText(Base):
    """富文本文章"""
    __tablename__ = "RichText"
    id = Column(String(64), primary_key=True)
    author_id = Column(String(64), comment='创建人id(管理员)')
    material_type = Column(Integer, comment='文章类型 material_type id')
    title = Column(Text, comment='标题')
    cover = Column(Text, url=True, comment='主图/封面')
    content = Column(LONGTEXT, comment='富文本内容')

    @property
    def material_type_zh(self):
        material_type = MaterialType.query.filter(MaterialType.isdelete == false(),
                                                  MaterialType.id == self.material_type
                                                  ).first()
        material_type_zh = material_type.name if material_type else ''
        return material_type_zh

    @orm.reconstructor
    def __init__(self):
        super(RichText, self).__init__()
        self.hide('author_id')
        self.add('material_type_zh')


class Media(Base):
    """媒体资源/作品展示/校园视频等"""
    __tablename__ = "Media"
    id = Column(String(64), primary_key=True)
    author_id = Column(String(64), comment='创建人id(管理员)')
    material_type = Column(Integer, comment='类型 material_type id')
    description = Column(Text, comment='简介')
    cover = Column(Text, url=True, comment='主图/视频封面')
    media_url = Column(Text, comment='媒体资源链接')

    @property
    def material_type_zh(self):
        material_type = MaterialType.query.filter(MaterialType.isdelete == false(),
                                                  MaterialType.id == self.material_type
                                                  ).first()
        material_type_zh = material_type.name if material_type else ''
        return material_type_zh

    @orm.reconstructor
    def __init__(self):
        super(Media, self).__init__()
        self.hide('author_id')
        self.add('material_type_zh')


class MaterialType(Base):
    """素材类型/标签"""
    __tablename__ = "MaterialType"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), comment='标签名')


class ContactsCard(Base):
    """联系我们"""
    __tablename__ = "ContactsCard"
    id = Column(String(64), primary_key=True)
    title = Column(String(100), comment='校区名')
    address = Column(String(255), comment='地址')
    longitude = Column(String(255), comment='经度')
    latitude = Column(String(255), comment='纬度')
    telephone = Column(String(15), comment='联系电话')
    fax = Column(String(200), comment='传真')
    website = Column(Text, comment='网址')
    mailbox = Column(String(60), comment='邮箱')
    headmaster = Column(String(20), comment='校长')
