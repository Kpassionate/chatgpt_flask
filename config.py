#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime


class Config(object):
    DEBUG = False
    JSON_AS_ASCII = False  # 这个配置可以确保http请求返回的json数据中正常显示中文
    SECRET_KEY = 'scd8^lub*29ds'
    TOKEN_EXPIRATION = 30 * 24 * 3600  # token 时长30天
    # JWT配置
    JWT_SECRET_KEY = 'ksogQP84'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)  # 过期时间


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@localhost/openai'  # 连接数据库
    SQLALCHEMY_POOL_SIZE = 5  # 连接池
    SQLALCHEMY_POOL_TIMEOUT = 15  # 连接超时等待时间
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 动态追踪修改设置，如未设置只会提示警告
    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True
    PROPAGATE_EXCEPTIONS = True
    # UPLOAD_FOLDER = '/static/uploads'


