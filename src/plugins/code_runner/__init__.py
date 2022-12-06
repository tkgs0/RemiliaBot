from html import unescape

from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    filters
)

from utils.log import logger
from .data_source import CodeRunner


def run(application):
    code_runner_handler = CommandHandler(
        'code', code_runner,
        filters.TEXT
    )
    application.add_handler(code_runner_handler)


async def code_runner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    opt = update.message.text.replace('/code', '', 1)
    if not opt:
        content = '发送 /code.help 查看帮助'
    elif opt == '.help':
        content = CodeRunner().help()
    elif opt == '.list':
        content = CodeRunner().list_supp_lang()
    else:
        content = str(await CodeRunner().runner(unescape(opt.strip())))
    await update.message.reply_text(content)

