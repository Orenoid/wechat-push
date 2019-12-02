import requests

from app.utils import cache


def send_template_message(openid, template_id, data, access_token):
    params = {'access_token': access_token}
    body = {
        'touser': openid,
        'template_id': template_id,
        'data': data
    }
    resp = requests.post(
        'https://api.weixin.qq.com/cgi-bin/message/template/send', params=params, json=body)


@cache(seconds=7000)
def get_access_token(appid, appsecret):
    params = {
        'grant_type': 'client_credential',
        'appid': appid,
        'secret': appsecret
    }
    resp = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=params)
    if resp.status_code != 200 or not resp.json().get('access_token'):
        raise Exception('获取access_token失败')
    return resp.json().get('access_token')
