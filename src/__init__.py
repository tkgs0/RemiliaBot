
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

datapath = Path().parent / 'data.json'
_data = json.loads(datapath.read_text("utf-8"))
TOKEN = _data['token']
NICKNAME = _data['nickname']


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f'Hello, This is {NICKNAME[0]}.'
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .plugins.status import Status
    msg, _ = Status().get_status()
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = msg
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .plugins.chat import reply
    msg = update.message.text
    content = await reply(msg, NICKNAME[0])
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = content
    )

async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .plugins.chat import reply
    msg = update.message.text
    for i in NICKNAME:
        if msg.startswith(i):
            msg = msg.lstrip(i)
            content = await reply(msg, NICKNAME[0])
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = content
            )


class run():
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    status_handler = CommandHandler('status', status)
    application.add_handler(status_handler)



    chat_handler = MessageHandler(
        filters.ChatType.PRIVATE & filters.TEXT & (~filters.COMMAND),
        chat
    )
    application.add_handler(chat_handler)

    groupchat_handler = MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & (~filters.COMMAND),
        groupchat
    )
    application.add_handler(groupchat_handler)

    
    application.run_polling()
