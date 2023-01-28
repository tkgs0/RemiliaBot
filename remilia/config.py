import yaml
from pathlib import Path
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    LOG_LEVEL: str = 'INFO'
    TOKEN: str = ''
    NICKNAME: list = ['remilia']
    SUPERUSERS: list = []
    SETU: dict = {'r18': 2, 'pixproxy': ''}
    ACGGOV: dict = {'token': 'apikey', 'pixproxy': ''}


default_config = """

LOG_LEVEL: 'DEBUG'

TOKEN: ''  # Telegram Bot API Token

NICKNAME:  # Bot的昵称
- Remilia
- Remi
- remilia
- remi

SUPERUSERS:  # Bot主人的 Telegram ID, ID为纯数字, 不是自己设置的用户名
- 123456
- 654321

SETU:
  r18: 2  # 0为非R18，1为R18，2为混合（在库中的分类，不等同于作品本身的R18标识）
  pixproxy: ''
  # pximg图片代理, 需要填写前缀 https:// 或 http://
  # 留空为直连 i.pximg.net

ACGGOV:
  token: ''
  pixproxy: ''

""".strip()


filepath = Path() / 'config.yml'


if not filepath.is_file():
    try:
        filepath.write_text(default_config, encoding='utf-8')
    except Exception as e:
        print('生成配置文件失败!\n'+repr(e))
    print('配置文件已生成, 请填写config.yml后重新启动Bot')
    exit(-1)


config = yaml.safe_load(filepath.read_text('utf-8'))

_config = Config.parse_obj(config)
LOG_LEVEL: str = _config.LOG_LEVEL
TOKEN: str = _config.TOKEN
NICKNAME: list = _config.NICKNAME
SUPERUSERS: list = _config.SUPERUSERS
SETU: dict = _config.SETU
ACGGOV: dict = _config.ACGGOV
