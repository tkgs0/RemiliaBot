from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from remilia.log import logger
from remilia.config import NICKNAME


def run(application):
    start_handler = CommandHandler(
        'start', start,
        filters.ChatType.PRIVATE
    )
    application.add_handler(start_handler)

    start1_handler = CommandHandler(
        'start', start1,
        ~filters.ChatType.PRIVATE
    )
    application.add_handler(start1_handler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    await update.message.reply_text(
        f'Hello, This is {NICKNAME[0]}.\n'
        f'Your Telegram ID is: {context._user_id}'
    )


async def start1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    await update.message.reply_text(f'The Chat ID is: {update.message.chat_id}')
