# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from flask import request
from .error_response import ParamsError


def parameter_required(required=None, others='allow', filter_none=True, forbidden=None, datafrom=None):
    """验证请求中必需的参数
    others: 如果是allow, 则代表不会清除其他参数
    filter_none: True表示会过滤到空值(空列表, 空字符串, None等除了0之外的False值)
    forbidden: 必需要清除的字段
    例如：
    required = ('latitude', 'longitude') return message: 必要参数缺失: 'latitude', 'longitude'
    required = {'latitude': '纬度', 'longitude': '经度'} return message: 请填写: 纬度, 经度
    required = 'latitude' return message: 必要参数缺失: 'latitude'
    """
    if datafrom is None:
        data = request.json or request.args.to_dict() or {}
    else:
        data = datafrom
    if filter_none:
        data = {
            k: v for k, v in data.items() if v or v == 0
        }
    if required:
        if isinstance(required, tuple):
            missed = list(filter(lambda x: x not in data, required))
            if missed:
                raise ParamsError('必要参数缺失: ' + ', '.join(missed))
        elif isinstance(required, dict):
            missed = [required.get(x) if required.get(x) else x for x in required.keys() if x not in data]
            if missed:
                raise ParamsError('请补全: ' + ', '.join(missed))
        elif isinstance(required, str):
            if required not in data:
                raise ParamsError('必要参数缺失: ' + required)
    if others != 'allow':
        data = {
            k: v for k, v in data.items() if k in required
        }
    if forbidden:
        data = {
            k: v for k, v in data.items() if k.lower() not in forbidden
        }
    return data


def validate_arg(regex, arg, msg=None):
    if arg is None:
        return
    res = re.match(regex, str(arg))
    if not res:
        raise ParamsError(msg)
    return arg


def validate_price(price, can_zero=True):
    """
    检验金额
    :param price: 金额
    :param can_zero: 是否可等于0
    :return: decimal object
    """
    if not re.match(r'(^[1-9](\d+)?(\.\d{1,2})?$)|(^0$)|(^\d\.\d{1,2}$)', str(price)) or float(price) < 0:
        raise ParamsError("数字'{}'错误， 只能输入不小于0的数字，最多可保留两位小数".format(price))
    if not can_zero and float(price) <= 0:
        raise ParamsError("数字'{}'错误， 只能输入大于0的数字，最多可保留两位小数".format(price))
    return Decimal(price).quantize(Decimal('0.00'))


def validate_chinese(name):
    """
    校验是否是纯汉字
    :param name:
    :return: 汉字, 如果有其他字符返回 []
    """
    re_chinese = re.compile(r'^[\u4e00-\u9fa5]{1,8}$')
    return re_chinese.findall(name)


def validate_telephone(telephone):
    """
    校验手机号
    :param telephone:
    :return: true
    """
    if not re.match(r'^1[0-9]{10}$', str(telephone)):
        raise ParamsError('手机号码格式错误，请检查后重新输入')


def validate_datetime(date):
    """判断是否是一个有效的日期字符串"""
    import time
    date = str(date)
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except Exception as e:
        print(e)
        return False
