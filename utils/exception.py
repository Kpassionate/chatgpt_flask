#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import json, request
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = '200'
    msg = 'success'
    data = ''

    def __init__(self, code=None, msg=None, data=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(self.msg, None)

    def get_body(self, *args, **kwargs):
        body = dict(
            msg=self.msg,
            code=self.code,
            request=request.method + ' ' + self.get_request_path()
        )
        return json.dumps(body)

    def get_headers(self, *args, **kwargs):
        """get a json header"""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_request_path():
        return str(request.full_path).split('?')[0]

    def get_response(self, *args, **kwargs) -> dict:
        response = dict(
            msg=self.msg,
            code=self.code,
            data=self.data
        )
        response = {k: v for k, v in response.items() if v}
        return response

    def __str__(self) -> str:
        return json.dumps(self.get_response())

    def __call__(self, *args, **kwargs):
        return self.get_response()


class Success(APIException):
    code = '200'
    msg = 'success'


class CreateSuccess(APIException):
    code = '201'  # 创建成功
    msg = 'created success'


class DeleteSuccess(APIException):
    code = '202'  # 删除成功  (204为删除成功状态码，但是其不返回任何值，为保持一致返回202)
    msg = 'delete success'


class ServerError(APIException):
    code = '500'  # 服务器错误
    msg = 'sorry, we made a mistake .'


class ClientError(APIException):
    code = '400'  # 客户端错误
    msg = 'clients is invalid'


class ParameterError(APIException):
    code = '101'  # 参数错误
    msg = 'invalid parameter'


class NotFound(APIException):
    code = '404'  # not found
    msg = 'the resource are not found o_o'


class MethodNotAllowed(APIException):
    code = '405'  # 请求方法不被允许
    msg = 'the request method is not allowed o_o'


class AuthFailed(APIException):
    code = '401'  # 授权失败 Unauthorized
    msg = 'not auth'


class Forbidden(APIException):
    code = '403'  # 无权限访问
    msg = 'not auth'


a = AuthFailed()()
print(a, type(a))