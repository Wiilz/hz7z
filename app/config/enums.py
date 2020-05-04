# -*- coding: utf-8 -*-
from ..extensions.base_enum import Enum


class TestEnum(Enum):
    ok = 66, '成功'


class AdminLevel(Enum):
    super = 1, '超级管理员'
    general = 2, '普通管理员'


class AdminStatus(Enum):
    normal = 0, '正常'
    frozen = 1, '已冻结'
    deleted = 2, '已删除'


if __name__ == '__main__':
    print(TestEnum(66).zh_value)
