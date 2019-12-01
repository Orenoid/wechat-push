import datetime

from flask import Blueprint, current_app, request
from flask_restful import Resource

from app.models import User, Channel
from app.utils.http import Api, result_formatter, success_result
from app.utils.wechat import send_template_message, get_access_token

api_bp = Blueprint('api', __name__)
api = Api(api_bp)


@api.resource('/push/msg')
class Message(Resource):
    method_decorators = [result_formatter]

    def post(self):
        msg_content = request.json.get('msg_content')
        channel_name = request.json.get('channel_name') or ''
        push_time = request.json.get('push_time')
        channel = Channel.query.filter_by(name=channel_name).first()
        if channel is None:
            return '频道未建立', 404
        users = channel.users.all()
        access_token = get_access_token(
            current_app.config['APPID'], current_app.config['APPSECRET'])
        template_id = current_app.config['TEMPLATE_ID']
        # json格式按照事先定好的模板消息组织的,详见微信文档
        message_data = {
            'first': {'value': channel_name},
            'keyword1': {'value': msg_content},
            'keyword2': {'value': push_time or datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}
        }
        for user in users:
            send_template_message(user.openid, template_id, message_data, access_token)
        return success_result
