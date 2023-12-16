from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler
from telegram.constants import ParseMode

import locale
import json

from API_helper import APIHelper
from models import TokenModel, MarketModel
from utils import get_token_from, get_token_with

locale.setlocale(locale.LC_ALL, 'en_US')
helper = APIHelper()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = f"""
Hello, {update.message.from_user.first_name}! This is bot used to get information about cryptocurrency!
With this bot you can get the latest information of specific cryptocurrency, also you can predict how a cryptocurrency perform in the next 24 hours.

To start using this bot you can choose one of our command:
    • /list – to list top 100 cryptocurrencies
    • /info – to get the latest information of specific cryptocurrency
    • /predict – to predict next 24 hours price of a specific cryptocurrency
    • /help – to list all available commands and how to use this bot
"""
    await update.message.reply_text(response)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = """
*List of commands:*
    • /start    : to start the bot
    • /help     : to show all available commands and how to use this bot
    • /list     : to list top 100 cryptocurrencies
    • /info     : to get the latest information of specific cryptocurrency
    • /predict  : to predict next 24 hours price of a specific cryptocurrency

*How to use bot:*
1\. If you want to __check price__ of a specific cryptocurrency use command /info, but if you want to __predict price __ use command /predict\. Then type in your cryptocurrency symbol or name and send\. \(You can use /list for reference\)
    a\) If there is more than one cryptocurrency with that symbol, then bot will send you a list of cryptocurrencies with that symbol along with it's name\. You can then type in the name of cryptocurrency you want to check or you can pick one from the inline keyboard that are located under the input box\.
    b\) If there is only one cryptocurrency with that symbol or the name of cryptocurrency that you have sent from previous point exist, then you will get the necessary information or prediction from the bot\.
        
    • After you get the necessary information the bot will stop the conversation and will only be able to check again when you use one of these commands: /info /predict\.
        
    • If you want to cancel the checking process you can use command /cancel or press the command from inline keyboard located under your input box\. You can cancel the process from any step\.
        
PS: If the name or symbol of cryptocurrency that you have entered doesn't exist then bot will send you an error message but bot will still be in conversation and you can send the correct or existing cryptocurrency name or symbol, or you can send word "Cancel" or use command /cancel to cancel checking and exit the conversation\.
    
2\. If you want to check the list of top 100 cryptocurrencies then use command /list\.     
"""
    await update.message.reply_text(response, parse_mode="markdownv2")

async def list_crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = ""
    tokens: [TokenModel] = helper.get_token_list_100()
    for i, token in enumerate(tokens[:100]):
        response += f'{i + 1}. {token.symbol.upper()} – {token.name}\n'
    print(f"Number of returned tokens{len(tokens)}")
    await update.message.reply_text(f'This command will return all list of cryptocurrencies.\n{response}')

async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = """
This command will return price prediction of a specific cryptocurrency whether it will rise or drop in the next 24 hours.
Please type in symbol or name of cryptocurrency you want to check.
Press /cancel or type Cancel to cancel finding information about currency.
"""
    await update.message.reply_text(
        response, 
        reply_markup=ReplyKeyboardMarkup(
            [['/cancel']], 
            one_time_keyboard=False
        )
    )
    return 1

async def cancel_predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Cancelled predicting price.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_predict_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    response = ""

    if text == 'Cancel':
        await update.message.reply_text('Cancelled predicting price.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    tokens_list = get_token_from(text)

    if not tokens_list:
        response = "Unfortunately we couldn't find any cryptocurrency with that name or symbol. Try another name or symbol or check our top 100 cryptocurrrency list by using /list command."
        await update.message.reply_text(response)

    if len(tokens_list) > 1:
        response = f"There are multiple cryptocurrency with symbol or name *{text.upper()}*, please pick one of the symbol!"
        keyboard_options = []
        row = []
        for i, token in enumerate(tokens_list):
            response += f"\n{i + 1}. {token.symbol.upper()} – {token.name}"
            row.append(f"{token.name}")
            if i % 2 == 1:
                keyboard_options.append(row)
                row = []

        if not keyboard_options or (row != [] and keyboard_options[-1] != row):
            keyboard_options.append(row)

        print(keyboard_options)
        await update.message.reply_text(
            response, 
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard_options, 
                one_time_keyboard=False,
                input_field_placeholder="Which one?"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        return 2
        
    if len(tokens_list) == 1:
        token: TokenModel = tokens_list[0]
        market: MarketModel = helper.get_price(token_id=token.id)

        if not market:
            response = "Error in server, please try again a bit later."
            await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        prediction = "rise" if market.price_change_percentage_24h >= 0.0 else "drop"
        response = f"Price of {market.symbol.upper()} – {market.name} will {prediction}!"
        print(f"Bot: {response}")

        await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    
async def predict_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Cancelled predicting price.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
    
async def handle_multiple_symbol_predict_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User: {update.message.id} in {message_type}: "{text}"')

    if text == 'Cancel':
        await update.message.reply_text('Cancelled predicting price.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
        
    token: TokenModel = get_token_with(name=text)
    if not token:
        await update.message.reply_text('Token with that name is not found. Please choose one of the option from the inline keyboard!')

    market: MarketModel = helper.get_price(token_id=token.id)

    if not market:
        response = "Error in server, please try again a bit later."
        await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    prediction = "rise" if market.price_change_percentage_24h >= 0.0 else "drop"
    response = f"Price of {market.symbol.upper()} – {market.name} will {prediction}!"
    print(f"Bot: {response}")

    await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = """
This command will return current information of a specific cryptocurrency.
Please type in symbol or name of cryptocurrency you want to check.
Press /cancel or type Cancel to cancel finding information about currency.
"""
    await update.message.reply_text(
        response, 
        reply_markup=ReplyKeyboardMarkup(
            [['/cancel']], 
            one_time_keyboard=False
        )
    )
    return 1

async def info_cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Cancelled looking for cryptocurrency information.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def handle_info_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User: {update.message.id} in {message_type}: "{text}"')

    if text == 'Cancel':
        await update.message.reply_text('Cancelled looking for cryptocurrency information.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    tokens_list = get_token_from(text)

    if not tokens_list:
        response = "Unfortunately we couldn't find any cryptocurrency with that name or symbol. Try another name or symbol or check our top 100 cryptocurrrency list by using /list command."
        await update.message.reply_text(response)

    if len(tokens_list) > 1:
        response = f"There are multiple cryptocurrency with symbol or name *{text.upper()}*, please pick one of the symbol!"
        keyboard_options = []
        row = []
        for i, token in enumerate(tokens_list):
            response += f"\n{i + 1}. {token.symbol.upper()} – {token.name}"
            row.append(f"{token.name}")
            if i % 2 == 1:
                keyboard_options.append(row)
                row = []

        if not keyboard_options or (row != [] and keyboard_options[-1] != row):
            keyboard_options.append(row)

        print(keyboard_options)
        await update.message.reply_text(
            response, 
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard_options, 
                one_time_keyboard=False,
                input_field_placeholder="Which one?"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
        return 2
        
    if len(tokens_list) == 1:
        token: TokenModel = tokens_list[0]
        market: MarketModel = helper.get_price(token_id=token.id)
        
        if not market:
            response = "Error in server, please try again a bit later."
            await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        price_change_symbol = '+' if market.price_change_percentage_24h > 0.0 else ''
        response = f"""
Here are the price info of token {market.symbol.upper()} – {market.name}:

Current price: {locale.currency(market.current_price, grouping=True)}
24 H price change: {price_change_symbol}{locale.currency(market.price_change_24h, grouping=True)} ({price_change_symbol}{market.price_change_percentage_24h:.2f} %)
Market cap: {locale.currency(market.market_cap, grouping=True)}
High 24 H: {locale.currency(market.high_24h, grouping=True)}
Low 24 H: {locale.currency(market.low_24h, grouping=True)}
        """

        print(f"Bot: {response}")

        await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


async def handle_multiple_symbol_info_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User: {update.message.id} in {message_type}: "{text}"')

    if text == 'Cancel':
        await update.message.reply_text('Cancelled looking for cryptocurrency information.', reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
        
    token: TokenModel = get_token_with(name=text)
    if not token:
        await update.message.reply_text('Token with that name is not found. Please choose one of the option from the inline keyboard!')

    market: MarketModel = helper.get_price(token_id=token.id)

    if not market:
        response = "Error in server, please try again a bit later."
        await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    price_change_symbol = '+' if market.price_change_percentage_24h > 0.0 else ''
    response = f"""
Here are the price info of token {market.symbol.upper()} – {market.name}:

Current price: {locale.currency(market.current_price, grouping=True)}
24 H price change: {price_change_symbol}{locale.currency(market.price_change_24h, grouping=True)} ({price_change_symbol}{market.price_change_percentage_24h:.2f} %)
Market cap: {locale.currency(market.market_cap, grouping=True)}
High 24 H: {locale.currency(market.high_24h, grouping=True)}
Low 24 H: {locale.currency(market.low_24h, grouping=True)}
        """

    print(f"Bot: {response}")

    await update.message.reply_text(response, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
