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
from telegram.constants import ParseMode
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
from openai import OpenAI, AsyncOpenAI
from telegram.constants import ParseMode, ChatType


async def gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.GROUP:
        if update.effective_message.text[:7] not in ['Вопрос.', 'вопрос.']:
            return
    if update.effective_user.id not in context.bot_data['student_ids']:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_text(no_user_hello_message),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return 
    user_text = update.effective_message.text
    if update.effective_chat.type == ChatType.GROUP:
        user_text = user_text[7:]
        if user_text[0] == ' ':
            user_text = user_text[1:]
    
    client = AsyncOpenAI()
    messages = [
        {"role": "developer", "content": [{"type": "text", "text": "Ты помощник репетитора по программированию и математике. В ответах, где ты хочешь вставить формулу, не пиши формулы в формате latex, а просто пиши выражение в виде: 2x*(3x-5)^2. Обычная замена уравнение символами. Перед * ставь пожалуйста \\."}]},
    ]
    

    if context.chat_data.get("previous_message"):
        messages.append(
            {"role": "user", "content": context.chat_data["previous_message"]}
        )
    if context.chat_data.get("context_message"):
        messages.append(
            {"role": "assistant", "content": context.chat_data["context_message"]}
        )

    messages.append({"role": "user", "content": user_text})

    completion = await client.chat.completions.create(model="gpt-4o", messages=messages)

    # print(completion.choices[0].message.content)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_text(completion.choices[0].message.content),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    context.chat_data["previous_message"] = user_text
    context.chat_data["context_message"] = completion.choices[0].message.content
