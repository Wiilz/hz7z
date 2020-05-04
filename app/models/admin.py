# -*- coding: utf-8 -*-
"""
create user: wiilz
create time:2020-05-04
"""

from sqlalchemy import Integer, String, Text, orm

from ..config.enums import AdminLevel, AdminStatus
from ..extensions.base_model import Base, Column


class Admin(Base):
    """管理员"""
    __tablename__ = 'Admin'
    id = Column(String(64), primary_key=True)
    name = Column(String(255), comment='管理员名')
    telephone = Column(String(13), comment='管理员联系电话')
    password = Column(String(255), nullable=False, comment='密码')
    avatar = Column(Text, comment='头像', url=True)
    level = Column(Integer, default=2, comment='管理员等级，{1: 超级管理员, 2: 普通管理员')
    status = Column(Integer, default=0, comment='账号状态，{0:正常, 1: 被冻结, 2: 已删除}')

    @orm.reconstructor
    def __init__(self):
        super(Admin, self).__init__()
        self.fields = ['name', 'avatar', 'level', 'status']
        if self.level:
            self.fill('level_zh', AdminLevel(self.level).zh_value)
        if self.status:
            self.fill('status_zh', AdminStatus(self.status).zh_value)
