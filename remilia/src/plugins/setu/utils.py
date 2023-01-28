from sys import exc_info
import httpx
from httpx import AsyncClient

from telegram import InputMediaPhoto

from remilia.log import logger


async def get_setu(tag=[], r18=0, num=1, pixproxy='') -> list:
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



async def down_pic(content, pixproxy):
    async with AsyncClient() as client:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }
        if not pixproxy:
            headers = {
                'Host': 'i.pximg.net',
                'Referer': 'https://www.pixiv.net/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }
        pics, status = list(), list()
        for i in content:
            res = await client.get(
                url = (
                    i['url'].replace('https://i.pixiv.re', pixproxy)
                    if pixproxy
                    else i['url'].replace('i.pixiv.re', 'i.pximg.net')
                ),
                headers=headers,
                timeout=30
            )
            if res.status_code == 200:
                logger.success(f'获取图片 {i["pid"]} 成功')
                pics.append([res.content, i['caption']])
            else:
                logger.error(sc := f'获取图片 {i["pid"]} 失败: {res.status_code}')
                status.append(sc)
            await res.aclose()
        return pics, status
