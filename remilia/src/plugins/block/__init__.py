from typing import Literal
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
from remilia.config import SUPERUSERS


file_path = Path() / 'data' / 'chatlist' / 'chatlist.json'
file_path.parent.mkdir(parents=True, exist_ok=True)

# 白名单
chatlist = (
    json.loads(file_path.read_text('utf-8'))
    if file_path.is_file()
    else {'chats': [], 'users': []}
)

CHATS = filters.Chat(chatlist['chats'])
USERS = filters.User(chatlist['users'])


def run(application):

    wake_handler = CommandHandler(
        'wake', wake,
        filters.User(SUPERUSERS))
    application.add_handler(wake_handler)

    sleep_handler = CommandHandler(
        'sleep', sleep,
        filters.User(SUPERUSERS))
    application.add_handler(sleep_handler)

    banUser_handler = CommandHandler(
        'dwu', banUser,
        filters.User(SUPERUSERS))
    application.add_handler(banUser_handler)

    unbanUser_handler = CommandHandler(
        'awu', unbanUser,
        filters.User(SUPERUSERS))
    application.add_handler(unbanUser_handler)

    banChat_handler = CommandHandler(
        'dwc', banChat,
        filters.User(SUPERUSERS))
    application.add_handler(banChat_handler)

    unbanChat_handler = CommandHandler(
        'awc', unbanChat,
        filters.User(SUPERUSERS))
    application.add_handler(unbanChat_handler)


    block_handler = MessageHandler(~(CHATS|USERS), block)
    application.add_handler(block_handler)


async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    handle_chatlist([update.message.chat_id,], 'add', 'chats')
    await update.message.chat.send_message('呜......醒来力...')


async def sleep(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    handle_chatlist([update.message.chat_id,], 'del', 'chats')
    await update.message.chat.send_message('那我先去睡觉了...')


async def banUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = handle_msg(context.args, 'del', 'users')
    await update.message.reply_text(msg)


async def unbanUser(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = handle_msg(context.args, 'add', 'users')
    await update.message.reply_text(msg)


async def banChat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = handle_msg(context.args, 'del', 'chats')
    await update.message.reply_text(msg)


async def unbanChat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'[{update.message.chat.type.upper()}]({update.message.chat_id}) {context._user_id}: {update.message.text}')
    msg = handle_msg(context.args, 'add', 'chats')
    await update.message.reply_text(msg)



async def block(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return



def save_chatlist() -> None:
    file_path.write_text(json.dumps(chatlist), encoding='utf-8')


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


def handle_msg(
    args,
    mode: Literal['add', 'del'],
    type_: Literal['users', 'chats'],
) -> str:
    if not args:
        return ('用法:\n/ban(/unban) uid uid1 uid2 ...\n'
            '/banc(/unbanc) uid uid1 uid2 ...')
    for uid in args:
        if not is_number(uid):
            return '参数错误, uid必须是数字..'
    args = [int(uid) for uid in args]
    msg = handle_chatlist(args, mode, type_)
    return msg


def handle_chatlist(
    args: list,
    mode: Literal['add', 'del'],
    type_: Literal['users', 'chats'],
) -> str:
    if mode == 'add':
        chatlist[type_].extend(args)
        chatlist[type_] = list(set(chatlist[type_]))
        _mode = '添加'

        if type_ == 'users': USERS.add_user_ids(args) 
        else: CHATS.add_chat_ids(args)

    else:
        chatlist[type_] = [uid for uid in chatlist[type_] if uid not in args]
        _mode = '删除'

        if type_ == 'users': USERS.remove_user_ids(args)
        else: CHATS.remove_chat_ids(args)

    save_chatlist()
    _type = '用户' if type_ == 'users' else '会话'

    return f"白名单{_mode} {len(args)} 个{_type}:\n{args}"

