
TOKEN = ''

NICKNAME = [
    'Remilia',
    'Remi',
    'remilia',
    'remi'
  ]

SUPERUSERS = [123456, 654321]

SETU = {
    # 0为非R18，1为R18，2为混合（在库中的分类，不等同于作品本身的R18标识）
    'r18': 2,
    # pximg图片代理, 需要填写前缀 https:// 或 http://
    # 默认为 https://i.pixiv.re
    'pixproxy': ''
}

def chatGPT_token():
    # 参考 https://github.com/acheong08/ChatGPT/wiki/Setup
    return {
        'Authorization': '<API-KEY>',
        'session_token': ''
    }
