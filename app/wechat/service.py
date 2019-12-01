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


def create_channel(channel_name):
    new_channel = Channel(name=channel_name)
    db.session.add(new_channel)
    db.session.flush()
    return new_channel


def bind_user_and_channel(user: User, channel: Channel):
    user.channels.append(channel)
    db.session.flush()
