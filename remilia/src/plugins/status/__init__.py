from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from remilia.src import scheduler
from remilia.log import logger
from remilia.config import SUPERUSERS
from .data_source import get_status


def run(application):
    status_handler = CommandHandler(
        'status', status,
        filters.User(SUPERUSERS)
    )
    application.add_handler(status_handler)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg, _ = await get_status()
    await update.message.reply_text(msg)


@scheduler.scheduled_job(
    "interval",
    id="状态检查",
    name="状态检查",
    minutes=30,
    misfire_grace_time=15
)
async def _():
    logger.info("检查资源消耗中...")
    msg, stat = await get_status()
    if not stat:
        logger.warning(msg)
    else:
        logger.info("资源消耗正常")

