import logging
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.constants import ParseMode, ChatType
from dotenv import load_dotenv

from texts import hello_message, no_user_hello_message
from support_func import escape_text

from constants import (
    MAINMENU,
    MAINMENU_ADMIN,
    GET_ADMIN_STUDENTS,
    GET_ADD_REPLACE_ANSWER,
    load_admin_ids,
    load_students_ids,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.GROUP:
        return ConversationHandler.END
    if update.effective_user.id in context.bot_data['admin_ids']:
        return await admin_menu(update, context)

    elif update.effective_user.id in context.bot_data['student_ids']:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_text(hello_message),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return MAINMENU
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_text(no_user_hello_message),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return ConversationHandler.END


async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Добавить ученика(ов)", callback_data="add_students")],
        [InlineKeyboardButton("Добавить админа", callback_data="add_admins")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_text("Это меню администратора."),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup,
    )

    return MAINMENU_ADMIN


async def admin_students_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data["status"] = query.data

    if query.data == "add_students":
        await query.edit_message_text(
            text=escape_text(
                "Введи id новых учеников, каждый на новой строке\n"
                + "\n".join(map(str, context.bot_data['student_ids']))
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    elif query.data == "add_admins":
        await query.edit_message_text(
            text=escape_text(
                "Введи id нового админа, каждый на новой строке\n"
                + "\n".join(map(str, context.bot_data['admin_ids']))
            ),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    return GET_ADMIN_STUDENTS


async def get_admin_students_ids(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.effective_message.text
    context.user_data["user_text"] = user_text

    keyboard = [
        [InlineKeyboardButton("Добавить", callback_data="add")],
        [InlineKeyboardButton("Заменить", callback_data="replace")],
    ]
    markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_text("Вы хотите добавить новых людей или заменить всех этими id"),
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=markup,
    )

    return GET_ADD_REPLACE_ANSWER


async def get_add_replace_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    status = context.user_data.get("status")
    if status == "add_students":
        file_path = "students.txt"
    elif status == "add_admins":
        file_path = "admin.txt"

    if query.data == "add":
        with open(file_path, "a") as f:
            f.write("\n".join(context.user_data["user_text"].split("\n")) + "\n")

    elif query.data == "replace":
        with open(file_path, "w") as f:
            f.write("\n".join(context.user_data["user_text"].split("\n")) + "\n")

    context.bot_data["admin_ids"] = load_admin_ids()
    context.bot_data["student_ids"] = load_students_ids()
    
    await query.delete_message()
    return await admin_menu(update, context)
