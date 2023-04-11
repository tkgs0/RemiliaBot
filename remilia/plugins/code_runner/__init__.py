from html import unescape

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from remilia.log import logger
from .data_source import CodeRunner


def run(application):
    code_runner_handler = CommandHandler(
        'code', code_runner,
        filters.TEXT
    )
    application.add_handler(code_runner_handler)


async def code_runner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    opt = (
        context.args[0] + update.message.text.split(context.args[0], 1)[1]
        if context.args else ''
    )
    if not opt:
        content = '发送 /code -h 查看帮助'
    elif opt == '-h':
        content = CodeRunner().help()
    elif opt == '-ls':
        content = CodeRunner().list_supp_lang()
    else:
        content = str(await CodeRunner().runner(unescape(opt)))
    await update.message.reply_text(content)

