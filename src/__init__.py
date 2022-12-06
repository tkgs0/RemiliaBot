import sys

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from utils.log import (
    logging,
    logger,
    LoguruHandler,
    default_format
)

from config import TOKEN, NICKNAME, SUPERUSERS


logging.basicConfig(handlers=[LoguruHandler()], level=logging.INFO)

logger.remove()
logger.add(sys.stdout, level='INFO', diagnose=False, format=default_format)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'\033[36;1mEvent\033[0m [{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    await context.bot.send_message(
        chat_id = update.message.chat_id,
        text = (
            f'Hello, This is {NICKNAME[0]}.\n'
            f'Your Telegram ID is: {context._user_id}'
    ))


from .plugins import (
    chat,
    cmd,
    setu,
    status
)

class run():
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler(
        'start', start,
        filters.ChatType.PRIVATE
    )
    application.add_handler(start_handler)

    status_handler = CommandHandler(
        'status', status.status,
        filters.User(SUPERUSERS)
    )
    application.add_handler(status_handler)

    cmd_handler = CommandHandler(
        'cmd', cmd.cmd,
        filters.TEXT & filters.User(SUPERUSERS)
    )
    application.add_handler(cmd_handler)

    setu_handler = CommandHandler('setu', setu.setu)
    application.add_handler(setu_handler)


    chat_handler = MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT & (~filters.COMMAND),
        chat.chat
    )
    application.add_handler(chat_handler)

    groupchat_handler = MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & (~filters.COMMAND),
        chat.groupchat
    )
    application.add_handler(groupchat_handler)


    application.run_polling()
