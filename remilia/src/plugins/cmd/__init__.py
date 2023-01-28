from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from remilia.log import logger
from remilia.config import SUPERUSERS
from .sys_cmd import shell


def run(application):
    cmd_handler = CommandHandler(
        'cmd', cmd,
        filters.TEXT & filters.User(SUPERUSERS)
    )
    application.add_handler(cmd_handler)


async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    opt = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else ''
    )
    content = shell(opt)
    await update.message.reply_text(content)
