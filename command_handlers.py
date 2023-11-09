from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! This is bot for crypto price tracker!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please type any text to start! Help menu will be here!')

async def list_crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This command will return all list of cryptocurrencies.')

async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This command will return prediction of a specific cryptocurrency.')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This command will return current information of a specific cryptocurrency')