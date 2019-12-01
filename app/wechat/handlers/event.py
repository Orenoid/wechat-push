from wechatpy.events import SubscribeEvent, BaseEvent
from wechatpy.replies import TextReply, create_reply

from app.models import db, transaction

from app.wechat.service import create_user


@transaction
def handle(event: BaseEvent):
    if isinstance(event, SubscribeEvent):
        create_user(event.source)
        db.session.commit()
        return create_reply('发送“link 频道名称”订阅频道', message=event)

