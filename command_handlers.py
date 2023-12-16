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
    await update.message.reply_text('Hello! This is bot for crypto price tracker!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type any text to start! Help menu will be here!')

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
        # data = open('market_sample_data.json', 'r')
        # json_data = json.load(data)
        # market = MarketModel(**json_data[0])
        # print(market)
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
