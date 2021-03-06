# -*- coding: utf-8 -*-
from flask import Flask
from flask import Blueprint
from flask_cors import CORS

from .api import Hello, File, Admin, Config, Materials, Forms
from .extensions.request_handler import error_handler, request_first_handler
from .config.secret import DefaltSettig
from .extensions.register_ext import register_ext
from .extensions.base_jsonencoder import JSONEncoder
from .extensions.base_request import Request


def register(app):
    bp = Blueprint(__name__, 'bp', url_prefix='/api')
    bp.add_url_rule('/hello/<string:string>', view_func=Hello.as_view('hello'))
    bp.add_url_rule('/file/<string:string>', view_func=File.as_view('file'))
    bp.add_url_rule('/admin/<string:string>', view_func=Admin.as_view('admin'))
    bp.add_url_rule('/config/<string:string>', view_func=Config.as_view('config'))
    bp.add_url_rule('/materials/<string:string>', view_func=Materials.as_view('materials'))
    bp.add_url_rule('/forms/<string:string>', view_func=Forms.as_view('forms'))
    app.register_blueprint(bp)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return resp


def create_app():
    app = Flask(__name__)
    app.json_encoder = JSONEncoder
    app.request_class = Request
    app.config.from_object(DefaltSettig)
    app.after_request(after_request)
    register(app)
    CORS(app, supports_credentials=True)
    request_first_handler(app)
    register_ext(app)
    error_handler(app)
    return app
