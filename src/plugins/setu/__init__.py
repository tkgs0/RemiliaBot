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
    if (tag := context.args) and is_number(tag[0]):
        num = int(tag[0])
        tag.remove(tag[0])
    else:
        tag = context.args
        num = 6
    content = await get_setu(
        tag=tag,
        r18=SETU['r18'],
        num=num,
        pixproxy=SETU['pixproxy']
    )
    if content[1] == 2:
        await update.message.reply_media_group(
            media = content[0],
            caption = content[2] if content[2] else None)
    elif content[1]:
        pic = content[0]
        await update.message.reply_photo(
            photo = pic[0],
            caption = pic[1] + ('\n'+content[2] if content[2] else ''))
    else:
        await update.message.reply_text(str(content[0]))


def is_number(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
