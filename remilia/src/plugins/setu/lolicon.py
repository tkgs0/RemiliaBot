from sys import exc_info
import httpx
from httpx import AsyncClient

from telegram import InputMediaPhoto

from remilia.log import logger
from remilia.config import SETU

from .download import down_pic


r18 = SETU['r18']
pixproxy = SETU['pixproxy']


async def get_setu(tag=[], num=1) -> list:
    logger.info('loading...')
    
    async with AsyncClient() as client:
        req_url = 'https://api.lolicon.app/setu/v2'
        params = {
            'tag': tag,
            'r18': r18,
            'size': 'regular',
            'num': num if num < 11 else 1
        }
        try:
            res = await client.get(req_url, params=params, timeout=30)
        except httpx.HTTPError as e:
            logger.warning(e)
            return [f'API异常{e}', False]
        try:
            logger.debug(content := res.json()['data'])
            _ = content[0]

            content = [{
                'pid': i['pid'],
                'url': i['urls']['regular'],
                'caption': (
                    f'标题: {i["title"]}\n'
                    f'pid: {i["pid"]}\n'
                    f'画师: {i["author"]}\n'
                    f'标签: {", ".join(i["tags"])}'
                )
            } for i in content]

            pics, status = await down_pic(content, pixproxy)

            logger.success('complete.')

            # if len(content) == 1:
            #     return [content[0]['url'], 1, content[0]['caption']]

            # media = [
            #     InputMediaPhoto(media=i['url'], caption=i['caption'])
            #     for i in content
            # ]
            # return [media, 2]

            if not pics:
                return ['\n'.join(status), False]
            if len(pics) == 1:
                return [pics[0], 1, '\n'.join(status) if status else '']

            media = [
                InputMediaPhoto(media=i[0], caption=i[1])
                for i in pics
            ]
            return [media, 2]

        except httpx.ProxyError as e:
            logger.warning(e)
            return [f'代理错误: {e}', False]
        except IndexError as e:
            logger.warning(e)
            return [f'图库中没有搜到关于{tag}的图。', False]
        except:
            logger.warning(f'{exc_info()[0]}, {exc_info()[1]}')
            return [f'{exc_info()[0]} {exc_info()[1]}。', False]
