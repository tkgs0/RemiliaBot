
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
    'pixproxy': ''
}

def chatGPT_token():
    # token获取方法参考 https://github.com/tkgs0/Telegram-Bot#
    return {
        'Authorization': '<API-KEY>',
        'session_token': ''
    }
