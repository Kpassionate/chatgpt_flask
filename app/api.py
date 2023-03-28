#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Blueprint
from flask_restx import Api
from app.views.user import ns as user_ns
from app.views.chat_openai import ns as openai_ns

api_v1 = Blueprint("api", __name__, url_prefix="/api")

api = Api(
    app=api_v1,
    version="1.0",
    title="OpenAI API",
    description="A simple Use ChatGPT build Openai API",
)

api.add_namespace(user_ns)
api.add_namespace(openai_ns)
