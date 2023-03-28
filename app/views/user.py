#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask_restx import Resource, fields, Namespace
from app.models.user import User
from utils.date_util import datetime_to_str
from utils.exception import ClientError, ParameterError, Success, NotFound, DeleteSuccess, CreateSuccess

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

ns = Namespace("user", description="用户中心")

login_model = ns.model('LoginModel', {
    'username': fields.String(max_length=50, required=True, description='用户名'),
    'password': fields.String(min_length=6, max_length=16, required=True, description='用户登录密码'),
})

# 校验字段
register_model = ns.inherit('RegisterModel', login_model, {
    'email': fields.String(max_length=64, description='邮箱')
})

user_model = ns.inherit('UserModel', register_model, {
    'id': fields.Integer(readonly=True),
    'is_active': fields.Integer(readonly=True),
    'created_at': fields.DateTime(readonly=True, dt_format='rfc822'),
    'updated_at': fields.DateTime(readonly=True, dt_format='rfc822')
})


@ns.route("/list", strict_slashes=False)
class UserList(Resource):
    # @ns.marshal_list_with(user_model, envelope='data')
    @staticmethod
    def get():
        """获取用户详情"""
        users = User.query.all()
        result = Success(data=[{
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': datetime_to_str(user.updated_at)
        } for user in users])
        return result()


@ns.route("/<uid>", strict_slashes=False)
class UserView(Resource):
    @jwt_required()
    def get(self, uid):
        """获取用户详情"""
        username = get_jwt_identity()
        print(username)
        user = User.query.filter_by(id=uid).first()
        result = Success(data={
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'created_at': datetime_to_str(user.updated_at)
        })
        return result()

    @ns.expect(user_model, validate=True)
    @jwt_required()
    def put(self, uid):
        """修改用户信息"""
        user = User.query.filter_by(id=uid).first()
        if not user:
            return NotFound(msg='用户不存在')()
        params = {k: v for k, v in ns.payload.items() if v}
        params.update({'id': uid})
        user = User(**params)
        user.update()
        return Success()()

    @jwt_required()
    def delete(self, uid):
        """删除用户"""
        user = User.query.filter_by(id=uid).first()
        user.delete()
        return DeleteSuccess()()


@ns.route("/register", strict_slashes=False)
class Register(Resource):
    @ns.doc('用户注册')
    @ns.expect(register_model, validate=True)
    def post(self):
        email = ns.payload.get('email')
        username = ns.payload.get('username')
        if not all([email, username]):
            return ParameterError()()
        user = User.query.filter_by(email=email).first()
        if user:
            return ClientError(msg='该邮箱已注册')()
        user = User.query.filter_by(username=username).first()
        if user:
            return ClientError(msg='该用户名已存在')()
        user = User(
            username=username,
            password=ns.payload.get('password'),
            email=email,
            is_active=1
        )
        user.save()
        return CreateSuccess(msg='注册成功,请重新登陆')()


@ns.route("/login")
class Login(Resource):
    @ns.doc(description="user login")
    @ns.expect(login_model, validate=True)
    def post(self):
        username = ns.payload.get('username')
        password = ns.payload.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                # 使用唯一且不可变的 username 作为identity的值
                access_token = create_access_token(identity=user.username)
                # 返回用户email 和 token值
                return Success(data={
                    'username': username,
                    'token': access_token
                })()
            else:
                return ClientError(msg='password error!')()
        else:
            return ParameterError(msg='user account not exist!')()
