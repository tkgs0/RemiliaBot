import random
from pathlib import Path
import ujson as json
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters
)

from remilia.log import logger
from remilia.config import SUPERUSERS, NICKNAME
from .utils import (
    xiaosi,
    xiaoai,
    get_chat_result,
    hello__reply
)
from .looklike import Look


confpath: Path = Path() / 'data' / 'smart_reply' / 'reply.json'
confpath.parent.mkdir(parents=True, exist_ok=True)

default_conf: dict = {'mode': 0}
conf: dict = (
    json.loads(confpath.read_text('utf-8'))
    if confpath.is_file() else default_conf
)
conf: dict = conf if conf.keys() == default_conf.keys() else default_conf


def save_conf() -> None:
    confpath.write_text(json.dumps(conf), encoding='utf-8')


def run(application):
    set_chat_handler = CommandHandler(
        'setreply', set_reply,
        filters.User(SUPERUSERS)
    )
    application.add_handler(set_chat_handler)

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


async def set_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = context.args[0] if context.args else ''

    if msg == '思知' or msg == '小思':
        conf['mode'] = 0
    elif msg == '小爱':
        conf['mode'] = 1
    elif not msg:
        conf['mode'] = 0 if conf['mode'] else 1
    else:
        await update.message.chat.send_message('模式不存在.')
        return

    save_conf()
    mode = ['小思', '小爱']
    await update.message.chat.send_message(f'已设置回复模式{mode[conf["mode"]]}')


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text.strip()
    content = await reply(msg, NICKNAME[0], context._user_id)
    if isinstance(content, str):
        await update.message.chat.send_message(content)
    else:
        await update.message.chat.send_voice(content)


async def groupchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = update.message.text
    for i in NICKNAME:
        if msg.startswith(i):
            msg = msg.replace(i, '', 1).strip()
            content = await reply(msg, NICKNAME[0], context._user_id)
            if isinstance(content, str):
                await update.message.chat.send_message(content)
            else:
                await update.message.chat.send_voice(content)


async def reply(msg: str, NICKNAME: str, uid: int):

    uid = uid

    if not conf['mode']:
        get_reply = xiaosi
    else:
        get_reply = xiaoai

    if not msg or msg in [
        "你好啊",
        "你好",
        "在吗",
        "在嗎",
        "在不在",
        "您好",
        "您好啊",
        "在",
    ]:
        return random.choice(hello__reply)
    if msg.startswith('你看我像'):
        return Look.like()
    # 从字典里获取结果
    result = await get_chat_result(msg)
    # 如果词库没有结果，则调用对话api获取回复
    if not result:
        content = await get_reply(msg, NICKNAME)
        return content
    return result

