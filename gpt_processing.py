from telegram import Update
from telegram.ext import (
    ContextTypes,
)
from telegram.constants import ParseMode

from texts import no_user_hello_message
from support_func import escape_text

from openai import AsyncOpenAI
from telegram.constants import ChatType


async def gpt_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type == ChatType.GROUP or update.effective_chat.id < 0:
        if update.effective_message.text[:7] not in ["Вопрос.", "вопрос."]:
            return
    if update.effective_user.id not in context.bot_data["student_ids"]:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=escape_text(no_user_hello_message),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        return
    user_text = update.effective_message.text
    if update.effective_chat.type == ChatType.GROUP:
        user_text = user_text[7:]
        if user_text[0] == " ":
            user_text = user_text[1:]

    client = AsyncOpenAI()
    messages = [
        {
            "role": "developer",
            "content": [
                {
                    "type": "text",
                    "text": "Ты помощник репетитора по программированию и математике. Если ты отправишь решение задачи ученику, то он его просто спишет и ничего не пойтет. В ответах, где ты хочешь вставить формулу, не пиши формулы в формате latex, а просто пиши выражение в виде: 2x*(3x-5)^2. Обычная замена уравнение символами. Перед * ставь пожалуйста \\. Если тебе отправляют задачу по программированию, то твоя задача не отвечать, рассказывать, как её решать, но НЕ ОТПРАВЛЯТЬ ЦЕЛОЕ РЕШЕНИЕ. Можешь приводить примеры НЕ СВЯЗАННЫЕ С ЭТОЙ ЗАДАЧЕЙ, рассказывать порядок действий, ПОКАЗАТЬ РЕШЕНИЕ ПОХОЖЕЙ ЗАДАЧИ. НЕ ОТПРАВЛЯТЬ решение именно этой задачи. На остальные вопросы по программированию отвечай, как считаешь нужным. На все вопросы кроме программирования и математики отвечай, что не можешь подсказать. Напиши функцию ... — это тоже решение задач. Что надо сделать ... — это тоже решение задач.",
                }
            ],
        },
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

    completion = await client.chat.completions.create(
        model="gpt-4o-mini", messages=messages
    )

    # print(completion.choices[0].message.content)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=escape_text(completion.choices[0].message.content),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    context.chat_data["previous_message"] = user_text
    context.chat_data["context_message"] = completion.choices[0].message.content
