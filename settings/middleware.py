#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import time
import datetime


class Middleware(object):
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        now = datetime.datetime.now()
        t1 = time.time()
        response = self.wsgi_app(environ, start_response)
        method = environ['REQUEST_METHOD']
        host = environ['HTTP_HOST']
        t2 = time.time()
        latency = round((t2 - t1) * 1000, 3)
        return response
