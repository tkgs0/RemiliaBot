from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from utils.log import logger
from src.config import SUPERUSERS
from .utils import ask, setgpt


def run(application):
    gpt_handler = CommandHandler(
        'gpt', gpt,
        filters.User(SUPERUSERS)
    )
    application.add_handler(gpt_handler)

    chatGPT_handler = CommandHandler('chat', chatGPT)
    application.add_handler(chatGPT_handler)


async def chatGPT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else 'About you'
    )
    user = str(context._user_id)
    content = await ask(user, msg)
    await update.message.reply_text(content)


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else ''
    )
    content = setgpt(msg)
    await update.message.reply_text(content)
