#!/user/bin/python
# _*_ coding:utf-8 _*_
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from app.api import api_v1
from app.views import user
from settings.config import DevConfig
from app.models.base import db
import time
import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)  # 实例化app
    # 加载配置(配置加载需要在初始化数据库之前，否则会报警告信息)
    app.config.from_object(DevConfig)
    # jwt 配置
    jwt = JWTManager(app)
    # 初始化数据库
    db.init_app(app)
    # 使用Migrate
    # manager = Manager(app)
    # migrate = Migrate(app, db)
    # manager.add_command('db', MigrateCommand)
    # db.create_all(app=app)  # 创建表结构
    # 注册api_v1蓝图
    app.register_blueprint(api_v1)
    # 添加日志处理器
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_formatter = logging.Formatter('%(levelname)s %(asctime)s [%(module)s:%(funcName)s] %(message)s')
    log_file = os.path.join(log_path, 'app-{}.log'.format(time.strftime('%Y-%m-%d')))
    log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 10, backupCount=10)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    app.logger.addHandler(log_handler)
    return app
