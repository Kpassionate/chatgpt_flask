import json
from app import create_app
from flask import request, jsonify

application = create_app()


# 中间件 <此响应之前的方法和flask_resx有冲突，先不使用>
# @application.before_request
# def get_request_info():
#     """请求"""
#     request_info = {
#         'method': request.method,
#         'url': request.url,
#         'params': request.json
#     }
#     application.logger.info(request_info)


@application.errorhandler(Exception)
def handle_value_error(e):
    """异常"""
    application.logger.error(str(e))
    if hasattr(e, 'code'):
        response = jsonify({'error': e.name + e.description})
        response.status_code = e.code
    else:
        response = jsonify({'error': str(e)})
        response.status_code = 500
    return response


@application.after_request
def handle_response(response):
    """响应"""
    status = response.status_code
    if status == 500:
        response = jsonify({'code': '500', 'error': json.loads(response.data)})
    elif status == 404:
        response = jsonify({'code': '404', 'error': '请求路径不存在'})
    elif status in [422, 405]:
        response = jsonify({'code': '101', 'error': '请求参数错误'})
    return response


if __name__ == "__main__":
    application.run()
