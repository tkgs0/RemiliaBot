import random
from telegram import Update
from telegram.ext import ContextTypes

from utils.log import logger
from config import NICKNAME
from .utils import get_reply, get_chat_result, hello__reply
from .looklike import Look


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'\033[36;1mEvent\033[0m [{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text
    content = await reply(msg, NICKNAME[0])
    await update.message.chat.send_message(content)


async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'\033[36;1mEvent\033[0m [{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text
    for i in NICKNAME:
        if msg.startswith(i):
            msg = msg.replace(i, '', 1)
            content = await reply(msg, NICKNAME[0])
            await update.message.chat.send_message(content)

async def reply(msg: str, NICKNAME: str):

    if (not msg) or msg.isspace() or msg in [
        "你好啊",
        "你好",
        "在吗",
        "在嗎",
        "在不在",
        "您好",
        "您好啊",
        "在",
    ]:
        return random.choice(hello__reply)
    if msg.startswith('你看我像'):
        return Look.like()
    # 从字典里获取结果
    result = await get_chat_result(msg)
    # 如果词库没有结果，则调用ownthink获取智能回复
    if result == None:
        url = f"https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken={msg}"
        content = await get_reply(url, NICKNAME)
        return content
    return result
