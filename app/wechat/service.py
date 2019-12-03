from app.models import User, db, Channel


def create_user(openid):
    user = User.query.filter_by(openid=openid).first()
    if user is not None:
        return user
    new_user = User(openid=openid)
    db.session.add(new_user)
    db.session.flush()
    return new_user


def subscribe_channel(openid, channel_name):
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        user = create_user(openid)

    channel = Channel.query.filter_by(name=channel_name).first()
    if channel is None:
        channel = create_channel(channel_name)
    bind_user_and_channel(user, channel)
    db.session.flush()


def unsubscribe_channel(openid, channel_name):
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        user = create_user(openid)
        return  # 用户不存在，自然没有订阅频道了

    channel = Channel.query.filter_by(name=channel_name).first()
    if channel is None:
        return '频道不存在'
    if user.channels.filter(Channel.name == channel_name).count() < 1:
        return '未订阅该频道'
    user.channels.remove(channel)
    if channel.user.count() == 0:
        Channel.query.filter_by(name=channel_name).delete()
    db.session.flush()


def create_channel(channel_name):
    new_channel = Channel(name=channel_name)
    db.session.add(new_channel)
    db.session.flush()
    return new_channel


def bind_user_and_channel(user: User, channel: Channel):
    user.channels.append(channel)
    db.session.flush()
