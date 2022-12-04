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
SUPERUSERS = _data['superusers']


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

async def cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .plugins.cmd import run
    msg = update.message.text.replace('/cmd', '', 1).strip()
    content = run(msg)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = content
    )

async def setu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from .plugins.setu import get_setu
    tag = context.args
    content = await get_setu(
        tag=tag,
        r18=_data['setu']['r18'],
        pixproxy=_data['setu']['pixproxy']
    )
    if content[1]:
        await context.bot.send_photo(
            chat_id = update.effective_chat.id,
            photo = content[0],
            caption = content[1]
        )
    else:
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = content[0]
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
            msg = msg.replace(i, '', 1)
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

    cmd_handler = CommandHandler(
        'cmd', cmd,
        filters.TEXT & filters.User(SUPERUSERS)
    )
    application.add_handler(cmd_handler)

    setu_handler = CommandHandler('setu', setu)
    application.add_handler(setu_handler)


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
