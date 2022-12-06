from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

from utils.log import logger
from config import SETU
from .utils import get_setu


def run(application):
    setu_handler = CommandHandler('setu', setu)
    application.add_handler(setu_handler)


async def setu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    tag = context.args
    content = await get_setu(
        tag=tag,
        r18=SETU['r18'],
        pixproxy=SETU['pixproxy']
    )
    if content[1]:
        await update.message.reply_photo(
            photo = content[0],
            caption = content[1]
        )
    else:
        await update.message.reply_text(content[0])

