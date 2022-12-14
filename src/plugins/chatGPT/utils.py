from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .revChatGPT import AsyncChatbot as Chatbot
import time
from src.config import chatGPT_token


CHATGPT = chatGPT_token()
chatbot = Chatbot(CHATGPT)


file_path = Path() / 'data' / 'chatGPT' / 'user_chat.json'
file_path.parent.mkdir(parents=True, exist_ok=True)

user_chat = (
    json.loads(file_path.read_text('utf-8'))
    if file_path.is_file()
    else dict()
)


def save_chat() -> None:
    file_path.write_text(json.dumps(user_chat), encoding='utf-8')


async def ask(user: str, msg: str):
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
            resp = await chatbot.get_chat_response(
                msg,
                conversation_id=user_chat[user]['cid'],
                parent_id=user_chat[user]['pid']
            )
        else:
            if msg in recmd:
                return '会话不存在'
            resp = await chatbot.get_chat_response(msg)

        user_chat.update({
            user: {
                'cid': chatbot.conversation_id,
                'pid': chatbot.parent_id,
                'time': time.time()
            }
        })
        save_chat()
        
        return resp['message'] if resp else '发生了一个错误, 返回值为空'

    except Exception as e:
        return repr(e)
