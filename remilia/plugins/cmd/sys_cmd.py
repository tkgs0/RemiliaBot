from platform import system
from subprocess import Popen, PIPE
from asyncio import create_subprocess_shell
from asyncio.subprocess import PIPE as AsyncPIPE
from html import unescape


cmd_help = '''
调用系统命令行
⚠危险操作, 谨慎使用!

/cmd {命令}
For example:
/cmd echo "Hello World"
'''.strip()


shell_help = '''
调用系统命令行
(不支持Windows)
⚠危险操作, 谨慎使用!

/sh {命令}
For example:
/sh echo "Hello World"
'''.strip()


def shell(opt: str) -> str:

    if not opt:
        return '发送 /cmd -h 获取帮助'

    if opt == '-h':
        return cmd_help

    content = Popen(
        unescape(opt.strip()),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        universal_newlines=True
    ).communicate()

    if content == ('',''):
        msg = '执行完毕, 没有任何输出呢~'
    elif not content[1]:
        msg = f'stdout:\n{content[0]}\n>执行完毕'
    elif not content[0]:
        msg = f'stderr:\n{content[1]}'
    else:
        msg = f'stdout:\n{content[0]}\nstderr:\n{content[1]}\n>执行完毕'
    return msg


_win = ('windows', 'Windows', 'win32', 'Win32', 'win16', 'Win16')


async def async_shell(opt: str) -> str:
    for i in _win:
        if system() and (system() in i or i in system()):
            return '暂不支持Windows,\n请使用同步方法 `/cmd`'

    if not opt:
        return '发送 /sh -h 获取帮助'

    if opt == '-h':
        return shell_help

    content = await (await create_subprocess_shell(
        unescape(opt.strip()),
        stdin=AsyncPIPE,
        stdout=AsyncPIPE,
        stderr=AsyncPIPE
    )).communicate()

    if content == (b'', b''):
        msg = '\n执行完毕, 没有任何输出呢~'
    elif content[1] == b'':
        msg = f'\nstdout:\n{content[0].decode()}\n>执行完毕'
    elif content[0] == b'':
        msg = f'\nstderr:\n{content[1].decode()}'
    else :
        msg = (f'\nstdout:\n{content[0].decode()}'
               f'\nstderr:\n{content[1].decode()}'
               '\n>执行完毕')
    return msg
