from telegram import Update
from telegram.ext import ContextTypes

from .sys_cmd import run
from utils.log import logger


async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'\033[36;1mEvent\033[0m [{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text.replace('/cmd', '', 1).strip()
    content = run(msg)
    await context.bot.send_message(
        chat_id = update.message.chat_id,
        text = content
    )
