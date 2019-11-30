from flask import Blueprint, request, current_app, abort, make_response, Response
from wechatpy import parse_message
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import TextReply
from wechatpy.utils import check_signature

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
        current_app.logger.exception('invalid')
        abort(400)

    return echostr


@wechat_bp.route('', methods=['POST'])
def post():
    msg = parse_message(request.data)
    current_app.logger.info(f'收到消息：{msg}')

    reply = TextReply(content='Confirmed', message=msg)
    xml = reply.render()
    return Response(xml, content_type='application/xml')
