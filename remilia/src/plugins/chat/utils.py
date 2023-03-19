import random
from pathlib import Path
import ujson as json
from httpx import AsyncClient
from string import punctuation, whitespace

from remilia.log import logger
from remilia.config import XIAOAI


# 载入词库(这个词库有点涩)
AnimeThesaurus = json.loads(
    (Path(__file__).parent / 'resource' / 'data.json').read_text("utf-8")
)

# hello之类的回复
hello__reply = [
    'ʕ  •ᴥ•ʔ ?',
]

# 从字典里返还消息, 借鉴(抄)的zhenxun-bot
async def get_chat_result(text: str):
    if len(text) < 7:
        keys = AnimeThesaurus.keys()
        for key in keys:
            if text.find(key) != -1:
                return random.choice(AnimeThesaurus[key])


# 从思知api拿到消息
async def xiaosi(msg: str, NICKNAME: str) -> str:

    # 将半角标点和空白符号换成全角空格
    for i in punctuation + whitespace:
        msg = msg.replace(i, '　')

    url = f'https://api.ownthink.com/bot'
    params = {
        'appid': 'xiaosi',
        'userid': 'user',
        'spoken': msg,
    }
    headers = {
        'referer': 'https://www.ownthink.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    async with AsyncClient() as client:
        try:
            response = await client.get(url=url, params=params, headers=headers)
            if response.json()['data']['type'] == 5000:
                res = response.json()['data']['info']['text'].replace('小思', NICKNAME)
                await response.aclose()
                return res
            return 'ʕ  •ᴥ•ʔ……'
        except Exception as e:
            logger.error(repr(e))
            return 'ʕ  •ᴥ•ʔ</>'


# 从小爱api拿到消息
async def xiaoai(msg: str, NICKNAME: str) -> str | bytes:

    # 将半角标点和空白符号换成全角空格
    for i in punctuation + whitespace:
        msg = msg.replace(i, '　')

    n: dict = XIAOAI['mp3']

    url = 'http://81.70.100.130/api/xiaoai.php'
    params = {
        'msg': msg,
        'n': 'mp3' if n else 'text',
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }

    async with AsyncClient() as client:
        try:
            response = await client.get(url=url, params=params, headers=headers)
            res, status = response.text, response.status_code
            await response.aclose()

            if status == 200:
                content = (
                    await get_voice(res)
                    if n
                    else res.replace('小爱', NICKNAME).replace('小米智能助理', '猫')
                )
                return content if content else 'ʕ  •ᴥ•ʔ</>'
            logger.error(res)

        except Exception as e:
            logger.error(repr(e))
        return 'ʕ  •ᴥ•ʔ</>'


async def get_voice(url: str) -> bytes | None:

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'content-type': 'audio/mpeg',
    }
    async with AsyncClient() as client:
        try:
            response = await client.get(url=url, headers=headers, timeout=60)
            res, status = response.content, response.status_code
            await response.aclose()
            if status == 200:
                return res
            logger.error(res.decode())
        except Exception as e:
            logger.error(repr(e))

