import telegram
from telegram import Update
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes

from utils import get_tg_bot_token
from command_handlers import *

tg_token = get_tg_bot_token()
bot = telegram.Bot(token=tg_token)

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
    app = Application.builder().token(tg_token).build()

    # commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('list', list_crypto_command))
    app.add_handler(CommandHandler('predict', predict_command))
    app.add_handler(CommandHandler('info', info_command))

    # messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # error
    app.add_error_handler(error)

    print('Bot is polling....')
    app.run_polling(poll_interval=3)