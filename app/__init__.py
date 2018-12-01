#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _mysql import DatabaseError

from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import logging
from config import config
from logging.handlers import RotatingFileHandler
from flask_wtf.csrf import CSRFProtect, generate_csrf

# 数据库
db = SQLAlchemy()


def create_app(config_name):
    """工厂模式"""

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    Session(app)

    # 开启CSRF保护
    CSRFProtect(app)

    @app.after_request
    def after_request(response):
        token = generate_csrf()
        response.set_cookie('csrf_token', token)
        return response

    # 启用日志
    setup_log(config_name)

    # # 注册蓝图
    # from .main.index import index_blue
    # app.register_blueprint(index_blue)


    @app.errorhandler(404)
    def page_not_found(error):
        pass
        # return render_template('news/404.html'), 404

    @app.errorhandler(DatabaseError)
    def special_exception_handler(error):
        db.session.rollback()
        app.logger.error(error)
        return 'Database connection failed', 500

    return app


def setup_log(config_name):
    """设置日志"""

    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级

    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)

    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')

    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)

    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


from . import model
