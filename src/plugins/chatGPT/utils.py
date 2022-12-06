from revChatGPT.revChatGPT import Chatbot
import time
from config import chatGPT_token

CHATGPT = chatGPT_token()

user_chat = dict()
'''
{
    user: [
        chatbot,
        time,
        conversation_id
    ]
}
'''

def ask(user: int, msg: str):
    if not CHATGPT['session_token']:
        return 'token未设置'

    if user in user_chat:
        start_time = user_chat[user][1]
        chatbot = user_chat[user][0]
        if time.time() > start_time + 60 * 3:
            # 如果上一次会话超过三分钟则开启新的会话
            chatbot.reset_chat()
    else:
        chatbot = Chatbot(CHATGPT, conversation_id=None)

    chatbot.refresh_session()
    resp = chatbot.get_chat_response(msg)
    user_chat.update({
        user: [
            chatbot,
            time.time()
        ]
    })
    return resp['message']
