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
from support_func import escape_text

from constants import MAINMENU, MAINMENU_ADMIN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in admin_ids:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Привет, админ!",
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return MAINMENU_ADMIN
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_text(hello_message),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    return MAINMENU
