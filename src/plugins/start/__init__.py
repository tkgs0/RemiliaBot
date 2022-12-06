from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from utils.log import logger
from config import NICKNAME


def run(application):
    start_handler = CommandHandler(
        'start', start,
        filters.ChatType.PRIVATE
    )
    application.add_handler(start_handler)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    await update.message.chat.send_message(
        f'Hello, This is {NICKNAME[0]}.\n'
        f'Your Telegram ID is: {context._user_id}'
    )
