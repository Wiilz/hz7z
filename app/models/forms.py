# -*- coding: utf-8 -*-
"""
create user: wiilz
create time:2020-05-04
"""

from sqlalchemy import String, Text, orm
from ..extensions.base_model import Base, Column


class Form(Base):
    """表单/信息提交"""
    __tablename__ = 'Form'
    id = Column(String(64), primary_key=True)
    name = Column(String(25), comment='姓名')
    telephone = Column(String(13), comment='电话')
    school = Column(String(200), comment='学校')
    remark = Column(Text, comment='备注')

    @orm.reconstructor
    def __init__(self):
        super(Form, self).__init__()
        self.add('createtime')


class FormImage(Base):
    """表单中的图片"""
    __tablename__ = 'FormImage'
    id = Column(String(64), primary_key=True)
    form_id = Column(String(64))
    url = Column(Text, url=True, comment='图片url')
