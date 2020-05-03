# -*- coding: utf-8 -*-
import re
import traceback
from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app, request
from .error_response import BaseError, SystemError
from .success_response import Success


def token_to_user_(token):
    user = None
    if token:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
            id = data['id']
            model = data['model']
            level = data['level']
            username = data.get('username', 'none')
            User = namedtuple('User', ('id', 'model', 'level', 'username'))
            user = User(id, model, level, username)
            setattr(request, 'user', user)
            current_app.logger.info('current_user info : {}'.format(data))
        except BadSignature as e:
            pass
        except SignatureExpired as e:
            pass
        except Exception as e:
            current_app.logger.info(e)
    current_app.logger.info(request.detail)
    return user


def request_first_handler(app):
    @app.before_request
    def token_to_user():
        current_app.logger.info('>>>>>>>>\n>>>>>>>>{}<<<<<<<<\n<<<<<<<<<<'.format('before request'))
        parameter = request.args.to_dict()
        token = parameter.get('token')
        user = token_to_user_(token)
        if token and not user:
            from ..extensions.error_response import TokenError
            raise TokenError('登录超时，请重新登录')


def error_handler(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        if isinstance(e, Success):
            return e
        if isinstance(e, Exception):
            data = traceback.format_exc()
            current_app.logger.error(data)
            # current_app.logger.error(data, exc_info=True)
        if isinstance(e, BaseError):
            return e
        else:
            if app.config['DEBUG']:
                return SystemError(e.args)
            return SystemError()
