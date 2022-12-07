import sys

from telegram.ext import ApplicationBuilder

from utils.log import (
    logging,
    logger,
    LoguruHandler,
    default_format
)
from config import TOKEN


logging.basicConfig(handlers=[LoguruHandler()], level=logging.INFO)

logger.remove()
logger.add(sys.stdout, level='INFO', diagnose=False, format=default_format)


from .plugins import (
    chat,
    chatGPT,
    cmd,
    code_runner,
    Gua64,
    setu,
    start,
    status
)

class run():
    app = ApplicationBuilder().token(TOKEN).build()


    start.run(app)
    cmd.run(app)
    status.run(app)
    code_runner.run(app)
    Gua64.run(app)
    setu.run(app)
    chatGPT.run(app)

    chat.run(app)


    app.run_polling()
