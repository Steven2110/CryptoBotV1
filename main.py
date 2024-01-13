import os

import telegram
from telegram import Update
from telegram.ext import Application, ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from utils import get_tg_bot_token
from command_handlers import *
from API_helper import APIHelper

tg_token = get_tg_bot_token()
bot = telegram.Bot(token=tg_token)

helper = APIHelper()

def handle_response(text: str) -> str:
    parsed = text.lower()

    if 'hello' in parsed:
        return 'Hey there!'
    
    return "I don't understand what you wrote"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User: {update.message.id} in {message_type}: "{text}"')

    response = handle_response(text)
    print(f"Bot: {response}")

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update: {update}, caused error {context.error}")

if __name__ == '__main__':
    print('Bot is starting')
    if os.stat('coins_data.json').st_size == 0:
        helper.get_token_list()

    app = Application.builder().token(tg_token).build()

    info_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('info', info_command)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_info_message)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_multiple_symbol_info_message)]
        },
        fallbacks=[CommandHandler('cancel', info_cancel_command)],
        allow_reentry=True
    )

    predict_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('predict', predict_command)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_predict_message)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_multiple_symbol_predict_message)]
        },
        fallbacks=[CommandHandler('cancel', predict_cancel_command)],
        allow_reentry=True
    )

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('list', list_crypto_command))
    app.add_handler(info_conv_handler)
    app.add_handler(predict_conv_handler)

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    print('Bot is polling....')
    app.run_polling(poll_interval=3)