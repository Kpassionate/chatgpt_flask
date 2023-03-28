#!/user/bin/python
# _*_ coding:utf-8 _*_
from flask import Flask
from flask_jwt_extended import JWTManager

from app.api import api_v1
from app.views import user
from config import DevConfig
from app.models.base import db


def create_app():
    app = Flask(__name__)  # 实例化app

    app.config.from_object(DevConfig)  # 加载配置(配置加载需要在初始化数据库之前，否则会报警告信息)
    jwt = JWTManager(app)
    db.init_app(app)  # 初始化数据库

    # manager = Manager(app)
    # migrate = Migrate(app, db)
    # manager.add_command('db', MigrateCommand)
    # db.create_all(app=app)  # 创建表结构
    # app.register_blueprint(book.mod, url_prefix='/api/book')  # 注册book蓝图
    app.register_blueprint(api_v1)  # 注册user蓝图

    return app

