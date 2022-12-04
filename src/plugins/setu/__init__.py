from sys import exc_info
import httpx
from httpx import AsyncClient
from loguru import logger

async def get_setu(tag=[], r18=0, pixproxy='') -> list:
    async with AsyncClient() as client:
        req_url = 'https://api.lolicon.app/setu/v2'
        params = {
            'tag': tag,
            'r18': r18,
            'size': 'regular'
        }
        try:
            res = await client.get(req_url, params=params, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [f'API异常{e}', False]
        try:
            setu_title = res.json()['data'][0]['title']
            setu_url = res.json()['data'][0]['urls']['regular']
            setu_pid = res.json()['data'][0]['pid']
            setu_author = res.json()['data'][0]['author']
            setu_tags = res.json()['data'][0]['tags']
            # p = res.json()['data'][0]['p']
            if pixproxy:
                setu_url = setu_url.replace('i.pixiv.re', pixproxy)
            pic = await down_pic(setu_url)
            data = (
                f'标题: {setu_title}\npid: {setu_pid}\n画师: {setu_author}\n标签: {", ".join(setu_tags)}'
                if type(pic) != int else ''
            )
            return [pic, data]
        except httpx.ProxyError as e:
            logger.warning(e)
            return [f'代理错误: {e}', False]
        except IndexError as e:
            logger.warning(e)
            return [f'图库中没有搜到关于{tag}的图。', False]
        except:
            logger.warning(f'{exc_info()[0]}, {exc_info()[1]}')
            return [f'{exc_info()[0]} {exc_info()[1]}。', False]


async def down_pic(url):
    async with AsyncClient() as client:
        headers = {
            'Referer': '',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 YaBrowser/23.7.7.77.77 SA/3 Safari/537.36'
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            logger.success('成功获取图片')
            return re.content
        else:
            logger.error(f'获取图片失败: {re.status_code}')
            return re.status_code

