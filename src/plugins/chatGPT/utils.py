from revChatGPT.revChatGPT import Chatbot
import time
from config import chatGPT_token


CHATGPT = chatGPT_token()

user_chat = dict()


def ask(user: int, msg: str):

    try:
        if user in user_chat:
            start_time = user_chat[user][1]
            chatbot = user_chat[user][0]
            if time.time() > start_time + 60 * 5:
                # 距上一次会话超过5分钟则开启新的会话
                chatbot.reset_chat()
        else:
            chatbot = Chatbot(CHATGPT, conversation_id=None)

        chatbot.refresh_session()
        resp = chatbot.get_chat_response(msg, output='text')
        user_chat.update({user: [chatbot, time.time()]})

        return resp['message']

    except Exception as e:
        return str(e)
