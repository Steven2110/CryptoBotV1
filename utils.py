import os
from dotenv import load_dotenv

def get_tg_bot_token() -> str:
    load_dotenv()
    bot_api_key = os.getenv('BOT_API_TOKEN')
    
    if bot_api_key:
        return bot_api_key
    else:
        raise Exception("API Token for Telegram bot is missing, please add it to environment variables file!")

    
