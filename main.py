import os
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from dotenv import load_dotenv


from callbacks import (
    start,
    admin_students_add,
    admin_menu,
    get_admin_students_ids,
    get_add_replace_answer,
)
from constants import (
    MAINMENU,
    MAINMENU_ADMIN,
    GET_ADMIN_STUDENTS,
    GET_ADD_REPLACE_ANSWER,
)
from constants import load_admin_ids, load_students_ids

from gpt_processing import gpt_message

load_dotenv()


if __name__ == "__main__":
    application = ApplicationBuilder().token(os.getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAINMENU: [],
            MAINMENU_ADMIN: [CallbackQueryHandler(admin_students_add)],
            GET_ADMIN_STUDENTS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_admin_students_ids),
                CommandHandler("skip", admin_menu),
            ],
            GET_ADD_REPLACE_ANSWER: [CallbackQueryHandler(get_add_replace_answer)],
        },
        fallbacks=[CommandHandler("start", start)],
        
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gpt_message))
    
    application.bot_data['admin_ids'] = load_admin_ids()
    application.bot_data['student_ids'] = load_students_ids()
    
    application.run_polling()
