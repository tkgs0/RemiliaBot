import random
from telegram import Update
from telegram.ext import (
    ContextTypes,
    MessageHandler,
    filters
)

from remilia.log import logger
from remilia.config import NICKNAME
from .utils import (
    get_reply,
    get_chat_result,
    hello__reply
)
from .looklike import Look


def run(application):
    chat_handler = MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT & (~filters.COMMAND),
        chat
    )
    application.add_handler(chat_handler)

    groupchat_handler = MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & (~filters.COMMAND),
        groupchat
    )
    application.add_handler(groupchat_handler)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text
    content = await reply(msg, NICKNAME[0])
    await update.message.chat.send_message(content)


async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
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
    # 如果词库没有结果，则调用对话api获取回复
    if not result:
        content = await get_reply(msg, NICKNAME)
        return content
    return result
