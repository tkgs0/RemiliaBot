from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from remilia.log import logger
from .Gua64 import encode, decode


def run(application):
    en64Gua_handler = CommandHandler(
        'en64', en64Gua,
        filters.TEXT
    )
    application.add_handler(en64Gua_handler)

    de64Gua_handler = CommandHandler(
        'de64', de64Gua,
        filters.TEXT
    )
    application.add_handler(de64Gua_handler)


async def en64Gua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else ''
    )
    content = encode(msg.encode()).decode() if msg else '需要内容'
    await update.message.reply_text(content)


async def de64Gua(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else ''
    )
    try:
        content = decode(msg.encode()).decode() if msg else '需要内容'
    except KeyError:
        content = '格式错误'
    await update.message.reply_text(content)

