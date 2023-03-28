#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from flask_restx import Resource, fields, Namespace
import openai

from app.models.openapi import OpenAI, Conversation
from utils.exception import Success, ParameterError
from utils.openai_util import davin_ci_003

ns = Namespace("openai", description="chat openai api")
openai.api_key = os.getenv('openai_key')

con_model = ns.model('ConModel', {
    'mid': fields.Integer(description='模型ID'),
    'uid': fields.Integer(description='用户ID'),
})

text_model = ns.model('TextModel', {
    'uid': fields.Integer(description='用户ID'),
    'cid': fields.Integer(description='会话ID'),
    'text': fields.String(max_length=500, required=True, description='文本输入'),
})


@ns.route("/conversation", strict_slashes=False)
class ConversationView(Resource):
    @ns.doc('建立对话')
    @ns.expect(con_model, validate=True)
    def post(self):
        uid = ns.payload.get('uid')
        mid = ns.payload.get('mid')
        if not all([uid, mid]):
            return ParameterError()()
        obj = Conversation(uid=uid, mid=mid)
        obj.save()
        # 返回会话ID
        c_obj = Conversation.query.filter_by(uid=uid, mid=mid).first()
        return Success(data=c_obj.id)()


@ns.route("/davin_ci", strict_slashes=False)
class DavinCiView(Resource):
    mid = 3

    @ns.doc('智能对话')
    @ns.expect(text_model, validate=True)
    def post(self):
        uid = ns.payload.get('uid')
        cid = ns.payload.get('cid')
        text = ns.payload.get('text')
        if not all([uid, cid, text]):
            return ParameterError()()
        # 初始化对话
        text = 'You: ' + text
        # 保存响应值
        base_params = {
            'uid': uid,
            'mid': self.mid,
            'cid': cid
        }
        req_obj = OpenAI(text=text, text_type=1, **base_params)
        req_obj.save()
        # 提取连续对话
        objs = OpenAI.query.filter_by(**base_params).order_by('created_at')
        text_list = [obj.text for obj in objs]
        ai_text = 'You: 你好呀?\nFriend: 你好!\n' + '\n'.join(text_list)
        DAVIN_CI003 = davin_ci_003(ai_text)
        # 获取openai响应
        resp = openai.Completion.create(**DAVIN_CI003)
        print(resp)
        resp_text = resp['choices'][0]['text'].strip()
        # 处理返回值
        resp_text = resp_text if 'Friend' in resp_text else 'Friend: ' + resp_text
        # 保存响应值
        resp_obj = OpenAI(text=resp_text, text_type=2, **base_params)
        resp_obj.save()
        data = resp_text.split('Friend: ')[1]
        return Success(data=data)()
