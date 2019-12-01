from wechatpy import create_reply
from wechatpy.messages import TextMessage

from app.models import User, transaction, db
from app.wechat.service import create_user, subscribe_channel


@transaction
def handle(msg: TextMessage):

    if msg.content.startswith('link '):
        channel_name = msg.content.replace('link ', '')
        subscribe_channel(openid=msg.source, channel_name=channel_name)
        db.session.commit()
        return create_reply('订阅成功', message=msg)
    else:
        return create_reply('不知道你在说什么', message=msg)
