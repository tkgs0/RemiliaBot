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
    msg = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else 'About you'
    )
    user = str(context._user_id)
    content = await ask(user, msg)
    await update.message.reply_text(content)

