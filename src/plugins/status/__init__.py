from telegram import Update
from telegram.ext import ContextTypes

from utils.log import logger
from .utils import Status


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg, _ = Status().get_status()
    await context.bot.send_message(
        chat_id = update.message.chat_id,
        text = msg
    )
