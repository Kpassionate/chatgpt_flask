#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 实例化数据库


class BaseModel(db.Model):
    __abstract__ = True  # 声明当前类为抽象类，可以被继承调用，不会被创建
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DATETIME, default=datetime.now())
    updated_at = db.Column(db.DATETIME, default=datetime.now())

    def __getitem__(self, item):
        return getattr(self, item)

    def keys(self):
        return self.fields if hasattr(self, 'fields') else []

    # 此函数作用？
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    # 增加
    def save(self):
        db.session.add(self)
        db.session.commit()

    # 修改
    def update(self):
        db.session.merge(self)
        db.session.commit()

    # 删除
    def delete(self):
        db.session.delete(self)
        db.session.commit()
