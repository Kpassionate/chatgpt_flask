from fluent import sender
from fluent import event

# from mainsys.settings import api_log
api_log = {'host': '101.43.157.127', 'port': 24224}

if api_log:
    host = api_log['host']
    port = api_log['port']
    # 此处的logs_app对应的是索引名称
    sender.setup('logs_app', host='101.43.157.127', port=24224)


# 记录日志
def send_log(log_data: dict):
    """
    :param log_data:{
        "clientIp": "客户端IP",
        "apiPath": "请求PATH",
        "requestTime": "请求时间",
        "totalLatency": "请求延迟",
        "request": "请求内容",
        "response": "返回数据",
        "statusCode": "返回状态码"
    }
    """
    # log_data['response'] = '{}'
    if api_log:
        event.Event('logs_ap', log_data)


if __name__ == "__main__":
    send_log({'aa': '444'})
