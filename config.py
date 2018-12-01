#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


class Config(object):
    """工程配置"""

    # 关系数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/code'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 设置日志级别
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产配置"""
    LOG_LEVEL = logging.ERROR


class DevelopmentConfig(Config):
    """开发配置"""
    DEBUG = True

    # 显示关系数据库操作信息
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True


# 定义配置字典
config = {
    'develpment': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}