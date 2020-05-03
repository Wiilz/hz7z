# -*- coding: utf-8 -*-
import os
import redis
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from .query_session import Query
from ..config.secret import DB_PARAMS
from .loggers import LoggerHandler


class SQLAlchemy(_SQLAlchemy):
    def init_app(self, app):
        app.config.setdefault('SQLALCHEMY_DATABASE_URI', DB_PARAMS)
        app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
        # app.config.setdefault('SQLALCHEMY_ECHO', True)  # 开启sql日志
        super(SQLAlchemy, self).init_app(app)

    @contextmanager
    def auto_commit(self):
        try:
            yield db.session
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy(query_class=Query, session_options={"expire_on_commit": False, "autoflush": False})

conn = redis.Redis(host='localhost', port=6379, db=1)


def register_ext(app, logger_file='/tmp/hz7z/'):
    db.init_app(app)
    LoggerHandler(app, file=logger_file).error_handler()
