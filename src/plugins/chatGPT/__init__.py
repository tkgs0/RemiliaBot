from telegram import Update
from telegram.ext import ContextTypes

from utils.log import logger
from .utils import ask


async def chatGPT(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'\033[36;1mEvent\033[0m [{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text.replace('/chatGPT', '', 1).strip()
    user = context._user_id
    content = ask(user, msg)
    await update.message.reply_text(content)

