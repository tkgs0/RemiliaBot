import httpx



RUN_API_URL_FORMAT = "https://glot.io/run/{}?version=latest"
SUPPORTED_LANGUAGES = {
    "assembly": {"ext": "asm"},
    "bash": {"ext": "sh"},
    "c": {"ext": "c"},
    "clojure": {"ext": "clj"},
    "coffeescript": {"ext": "coffe"},
    "cpp": {"ext": "cpp"},
    "csharp": {"ext": "cs"},
    "erlang": {"ext": "erl"},
    "fsharp": {"ext": "fs"},
    "go": {"ext": "go"},
    "groovy": {"ext": "groovy"},
    "haskell": {"ext": "hs"},
    "java": {"ext": "java", "name": "Main"},
    "javascript": {"ext": "js"},
    "julia": {"ext": "jl"},
    "kotlin": {"ext": "kt"},
    "lua": {"ext": "lua"},
    "perl": {"ext": "pl"},
    "php": {"ext": "php"},
    "python": {"ext": "py"},
    "ruby": {"ext": "rb"},
    "rust": {"ext": "rs"},
    "scala": {"ext": "scala"},
    "swift": {"ext": "swift"},
    "typescript": {"ext": "ts"},
}


class CodeRunner():

    @staticmethod
    def help() -> str:
        return (
            "/code {语言}\n"
            "{代码}\n"
            "For example:\n"
            "/code python\n"
            "print('hello world')\n\n"
            "发送 /code -ls 查看支持的语言"
        )

    @staticmethod
    def list_supp_lang() -> str:
        msg0 = "咱现在支持的语言如下：\n"
        msg0 += ", ".join(map(str, SUPPORTED_LANGUAGES.keys()))
        return msg0

    @staticmethod
    async def runner(msg: str):
        args = msg.split("\n")

        if not args or len(args) == 1:
            return "请检查输入内容...发送 /code -h 查看帮助"

        if (lang := args[0].strip()) not in SUPPORTED_LANGUAGES:
            return "该语言暂不支持...或者可能格式错误？"

        del args[0]
        code = "\n".join(map(str, args))
        url = RUN_API_URL_FORMAT.format(lang)
        js = {
            "files": [
                {
                    "name": (
                        SUPPORTED_LANGUAGES[lang].get("name", "main")
                        + f".{SUPPORTED_LANGUAGES[lang]['ext']}"
                    ),
                    "content": code,
                }
            ],
            "stdin": "",
            "command": "",
        }

        try:
            res = httpx.post(url, json=js)
        except Exception as e:
            return repr(e)

        payload = res.json()
        res.close()

        sent = False
        for k in ["stdout", "stderr", "error"]:
            v = payload.get(k)
            lines = v.splitlines()
            lines, remained_lines = lines[:10], lines[10:]
            out = "\n".join(lines)
            out, remained_out = out[: 60 * 10], out[60 * 10 :]

            if remained_lines or remained_out:
                out += f"\n（太多了太多了...）"

            if out:
                return f"{k}:\n{out}"

        if not sent:
            return "运行完成，没任何输出呢..."
