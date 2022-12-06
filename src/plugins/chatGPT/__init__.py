from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

from utils.log import logger
from .utils import ask


def run(application):
    chatGPT_handler = CommandHandler('chat', chatGPT)
    application.add_handler(chatGPT_handler)


async def chatGPT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text.replace('/chat', '', 1).strip()
    user = context._user_id
    content = ask(user, msg)
    await update.message.reply_text(content)

