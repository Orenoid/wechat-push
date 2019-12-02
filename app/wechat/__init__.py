import importlib

from flask import Blueprint, request, current_app, abort, make_response, Response
from wechatpy import parse_message
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply, BaseReply
from wechatpy.utils import check_signature

from app.wechat.exception import catch_err_when_handling_wechat_msg

wechat_bp = Blueprint('wechat', __name__)


@wechat_bp.route('', methods=['GET'])
def get():
    token = current_app.config.get('WECHAT_TOKEN')
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        current_app.logger.exception('invalid signature')
        abort(400)

    return echostr


@wechat_bp.route('', methods=['POST'])
@catch_err_when_handling_wechat_msg
def post():
    msg = parse_message(request.data)
    current_app.logger.info(f'收到消息：{msg}，消息类型：{type(msg)}')
    msg_type = msg.type
    try:
        handler = importlib.import_module(f'app.wechat.handlers.{msg_type}')
    except ModuleNotFoundError:
        current_app.logger.warning(f'未处理消息类型：{msg_type}')
        return 'SUCCESS'
    if hasattr(handler, 'handle'):
        reply = handler.handle(msg)
    else:
        raise AttributeError(f'handlers.{msg_type}模块未实现handle函数')

    if isinstance(reply, BaseReply):
        xml = reply.render()
        return Response(xml, content_type='application/xml')
    else:
        return reply or 'SUCCESS'
