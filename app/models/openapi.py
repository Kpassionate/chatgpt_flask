#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, String

from .base import db, BaseModel


class OpenAI(BaseModel):
    """AI"""
    __tablename__ = 'openai'
    uid = Column(db.INTEGER)
    mid = Column(db.INTEGER)
    cid = Column(db.INTEGER)
    text = Column(db.Text)
    text_type = Column(db.INTEGER)

    def __str__(self):
        return self.id


class Conversation(BaseModel):
    """会话"""
    uid = Column(db.INTEGER)
    mid = Column(db.INTEGER)

    def __str__(self):
        return self.id
