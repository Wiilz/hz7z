# -*- coding: utf-8 -*-
from ..extensions.base_enum import Enum


class TestEnum(Enum):
    ok = 66, '成功'


if __name__ == '__main__':
    print(TestEnum(66).zh_value)
