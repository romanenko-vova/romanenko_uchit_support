import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode
from dotenv import load_dotenv

from texts import hello_message

from callbacks import start
from my_logging import logger
from constants import MAINMENU, MAINMENU_ADMIN

load_dotenv()


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={MAINMENU: [], MAINMENU_ADMIN: []},
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    application.run_polling()
