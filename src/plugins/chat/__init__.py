import random
from .utils import get_reply, get_chat_result, hello__reply


async def reply(msg: str, NICKNAME: str):

    if (not msg) or msg.isspace() or msg in [
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
    # 从字典里获取结果
    result = await get_chat_result(msg)
    # 如果词库没有结果，则调用ownthink获取智能回复
    if result == None:
        url = f"https://api.ownthink.com/bot?appid=xiaosi&userid=user&spoken={msg}"
        content = await get_reply(url, NICKNAME)
        return content
    return result
