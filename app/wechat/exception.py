from functools import wraps

from flask import Response, request, current_app
from wechatpy import create_reply, parse_message


def catch_err_when_handling_wechat_msg(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        msg = parse_message(request.data)
        try:
            return func(*args, **kwargs)
        except Exception:
            current_app.logger.exception('处理微信消息出错')
            reply = create_reply('系统故障，请稍后再试', message=msg)
            return Response(reply.render(), content_type='application/xml')

    return wrapper
