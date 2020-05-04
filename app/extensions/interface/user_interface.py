from flask import request
from ...extensions.error_response import AuthorityError, TokenError


def is_anonymous():
    """是否是游客"""
    return not hasattr(request, 'user')


def token_required(func):
    def inner(*args, **kwargs):
        if not is_anonymous():
            return func(*args, **kwargs)
        raise TokenError()

    return inner


def is_admin():
    """是否是管理员"""
    return hasattr(request, 'user') and request.user.model == 'Admin'


def admin_required(func):
    def inner(*args, **kwargs):
        if not is_admin():
            raise AuthorityError()
        return func(*args, **kwargs)

    return inner
