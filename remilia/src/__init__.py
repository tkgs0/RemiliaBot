import sys

from telegram.ext import ApplicationBuilder

from remilia.log import (
    logging,
    logger,
    LoguruHandler,
    default_format
)
from remilia.config import LOG_LEVEL, TOKEN


logging.basicConfig(handlers=[LoguruHandler()], level=logging.DEBUG)

logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL, diagnose=False, format=default_format)


from .plugins import (
    block,
    chat,
    cmd,
    code_runner,
    Gua64,
    pix,
    setu,
    start,
    status
)

class run():
    app = ApplicationBuilder().token(TOKEN).build()


    start.run(app)
    block.run(app)
    cmd.run(app)
    status.run(app)
    code_runner.run(app)
    Gua64.run(app)
    pix.run(app)
    setu.run(app)

    chat.run(app)


    app.run_polling()
