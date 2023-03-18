import yaml
from pathlib import Path
from pydantic import BaseModel, Extra
from typing import List, Dict


class Config(BaseModel, extra=Extra.ignore):
    ConfigVersion: str = ''
    LOG_LEVEL: str = 'INFO'
    TOKEN: str = ''
    NICKNAME: List[str] = ['remilia']
    SUPERUSERS: List[int] = []
    SETU: Dict = {'r18': 2, 'pixproxy': ''}
    ACGGOV: Dict = {'token': 'apikey', 'pixproxy': ''}
    XIAOAI: Dict = {'mp3': False}


default_config = """

ConfigVersion: '1.0.1'

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

XIAOAI: 
  mp3: false  # 当 mp3 为 true 时尝试使用语音发送

""".strip()


filepath = Path() / 'config.yml'


if not filepath.is_file():
    try:
        filepath.write_text(default_config, encoding='utf-8')
    except Exception as e:
        print('生成配置文件失败!\n'+repr(e))
    print('配置文件已生成, 请填写 config.yml 后重新启动Bot')
    exit(-1)


config = yaml.safe_load(filepath.read_text('utf-8'))

_config = Config.parse_obj(config)


if _config.ConfigVersion != Config.parse_obj(
    yaml.safe_load(default_config)
).ConfigVersion:
    print('config.yml 文件有更新, 请备份并删除后重新启动Bot')
    exit(-1)


LOG_LEVEL: str = _config.LOG_LEVEL
TOKEN: str = _config.TOKEN
NICKNAME: List[str] = _config.NICKNAME
SUPERUSERS: List[int] = _config.SUPERUSERS
SETU: Dict = _config.SETU
ACGGOV: Dict = _config.ACGGOV
XIAOAI: Dict = _config.XIAOAI
