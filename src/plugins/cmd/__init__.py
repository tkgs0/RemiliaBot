from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from utils.log import logger
from config import SUPERUSERS
from .sys_cmd import shell


def run(application):
    cmd_handler = CommandHandler(
        'cmd', cmd,
        filters.TEXT & filters.User(SUPERUSERS)
    )
    application.add_handler(cmd_handler)


async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text.replace('/cmd', '', 1).strip()
    content = shell(msg)
    await update.message.reply_text(content)
