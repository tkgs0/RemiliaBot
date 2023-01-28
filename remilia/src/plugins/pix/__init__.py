from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler
)

from remilia.log import logger
from .utils import get_pix


def run(application):
    pix_handler = CommandHandler('pix', pix)
    application.add_handler(pix_handler)


async def pix(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    if (keyword := context.args) and is_number(keyword[0]):
        num = int(keyword[0])
        keyword.remove(keyword[0])
    else:
        keyword = context.args
        num = 1

    content = await get_pix(keyword=keyword, img=num)

    if content[1] == 2:
        try:
            await update.message.reply_media_group(
                media = content[0],
                read_timeout = 60,
                write_timeout = 60,
                connect_timeout = 60,
                pool_timeout = 60,
            )
        except Exception as e:
            await update.message.chat.send_message(repr(e))
    elif content[1]:
        await update.message.reply_photo(
            photo = content[0][0],
            caption = content[0][1] + content[2]
        )
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
