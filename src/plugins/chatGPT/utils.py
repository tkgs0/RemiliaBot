from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .revChatGPT import AsyncChatbot as Chatbot
import time


conf_path = Path() / 'data' / 'chatGPT' / 'conf.json'
conf_path.parent.mkdir(parents=True, exist_ok=True)

CHATGPT = (
    json.loads(conf_path.read_text('utf-8'))
    if conf_path.is_file()
    else {'session_token': ''}
)


file_path = Path() / 'data' / 'chatGPT' / 'user_chat.json'
file_path.parent.mkdir(parents=True, exist_ok=True)

user_chat = (
    json.loads(file_path.read_text('utf-8'))
    if file_path.is_file()
    else dict()
)


def save_conf() -> None:
    conf_path.write_text(
        json.dumps(CHATGPT, ensure_ascii=False),
        encoding='utf-8'
    )


def save_chat() -> None:
    file_path.write_text(json.dumps(user_chat), encoding='utf-8')


async def ask(user: str, msg: str) -> str:
    if not CHATGPT['session_token']:
        return '未设置token'

    chatbot = Chatbot(CHATGPT)
    try:
        recmd = ['重置会话', '重設對談']
        if user in user_chat:
            start_time = user_chat[user]['time']
            if msg in recmd:
                if time.time() > start_time + 60 * 5:
                    user_chat.pop(user)
                    save_chat()
                    return '会话已重置'
                else:
                    return '重置选项冷却中...'
            resp, token = await chatbot.get_chat_response(
                msg,
                conversation_id=user_chat[user]['cid'],
                parent_id=user_chat[user]['pid']
            )
        else:
            if msg in recmd:
                return '会话不存在'
            resp, token = await chatbot.get_chat_response(msg)

        user_chat.update({
            user: {
                'cid': chatbot.conversation_id,
                'pid': chatbot.parent_id,
                'time': time.time()
            }
        })
        CHATGPT['session_token'] = token
        save_conf()
        save_chat()
        return resp['message'] if resp else '发生了一些问题, 返回值为空'

    except Exception as e:
        return repr(e)

def setgpt(msg: str) -> str:
    if msg.startswith('设置token'):
        token = msg.replace('设置token', '').strip()
        CHATGPT['session_token'] = token
        save_conf()
        return 'Done.'
    if msg.startswith('设置proxy'):
        proxy = msg.replace('设置proxy', '').strip()
        if proxy:
            CHATGPT['proxy'] = proxy
        else:
            CHATGPT.pop('proxy')
        save_conf()
        return 'Done.'
    if msg.startswith('设置UA'):
        ua = msg.replace('设置UA', '').strip()
        if ua:
            CHATGPT['user_agent'] = ua
        else:
            CHATGPT.pop('user_agent')
        save_conf()
        return 'Done.'
    if msg.startswith('设置lang'):
        lang = msg.replace('设置lang', '').strip()
        if lang:
            CHATGPT['accept_language'] = lang
        else:
            CHATGPT.pop('accept_language')
        save_conf()
        return 'Done.'
    return 'ʕ  •ᴥ•ʔ ?'
