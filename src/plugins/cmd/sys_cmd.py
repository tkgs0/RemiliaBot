import os
from subprocess import Popen, PIPE
from html import unescape


def help() -> str:
    return (
        "调用系统命令行\n"
        "⚠危险操作, 谨慎使用!\n\n"
        "/cmd [-s] {命令}\n"
        "  -s 无日志输出\n"
        "For example:\n"
        "/cmd echo \"Hello World\""
    )


def run(opt: str) -> str:

    if not opt:
        return "发送 /cmd.help 获取帮助"

    if opt.startswith(".help"):
        return help()

    if opt.startswith('-s'):
        opt = opt.replace('-s','',1)
        if (opt.startswith(' ') or opt.startswith('\n')) and (opt := opt.lstrip().lstrip('\n')) != '':
            content = os.system(unescape(opt))
            return "\n执行完毕: "+str(content)
        else:
            return "格式错误, 发送 /cmd.help 获取帮助"

    content = Popen(
        unescape(opt),
        stdin=PIPE,
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        universal_newlines=True
    ).communicate()

    if content == ('',''):
        msg = "\n执行完毕, 没有任何输出呢~"
    elif content[1] == '':
        msg = f"\nstdout:\n{content[0]}\n>执行完毕"
    elif content[0] == '':
        msg = f"\nstderr:\n{content[1]}"
    else :
        msg = f"\nstdout:\n{content[0]}\nstderr:\n{content[1]}\n>执行完毕"
    return msg


