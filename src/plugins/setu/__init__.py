from telegram import Update
from telegram.ext import ContextTypes

from utils.log import logger
from config import SETU
from .utils import get_setu


async def setu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    tag = context.args
    content = await get_setu(
        tag=tag,
        r18=SETU['r18'],
        pixproxy=SETU['pixproxy']
    )
    if content[1]:
        await context.bot.send_photo(
            chat_id = update.message.chat_id,
            photo = content[0],
            caption = content[1]
        )
    else:
        await context.bot.send_message(
            chat_id = update.message.chat_id,
            text = content[0]
        )

