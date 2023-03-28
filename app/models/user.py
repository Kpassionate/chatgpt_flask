#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, String

from .base import db, BaseModel


class User(BaseModel):
    username = Column(db.String(20), unique=True, nullable=False)
    _password = Column(db.String(100), nullable=False)  # 内部使用
    email = Column(db.String(24), unique=True, nullable=False)
    is_active = Column(db.INTEGER)

    def __str__(self):
        return self.username

    def keys(self):
        return ['id', 'username', 'email']

    @property
    def password(self):  # 外部使用：取值
        return self._password

    @password.setter
    def password(self, raw):  # 外部使用：赋值
        self._password = generate_password_hash(raw)

    def check_password(self, raw):  # 密码验证
        print(raw, self._password)
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
