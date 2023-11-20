import os
from dotenv import load_dotenv
import json
from models import TokenModel

def get_tg_bot_token() -> str:
    load_dotenv()
    bot_api_key = os.getenv('BOT_API_TOKEN')
    
    if bot_api_key:
        return bot_api_key
    else:
        raise Exception("API Token for Telegram bot is missing, please add it to the environment variables file!")

def get_cg_token() -> str:
    load_dotenv()
    coin_gecko_api_key = os.getenv('CG_API_TOKEN')

    if coin_gecko_api_key:
        return coin_gecko_api_key
    else:
        raise Exception("API Token for Coin Gecko is missing, please add it to the environment variables file!")
    
def clear_cache():
    open('coins_data.json', 'w').close()

def get_tokens_list_from_files() -> [TokenModel]:
    cache_file = open('coins_data.json', 'r')
    json_data = json.load(cache_file)

    tokens = []
    for token in json_data:
        tokens.append(TokenModel(**token))

    return tokens
    
def get_token_from(string: str) -> [TokenModel]:
    tokens_list = get_tokens_list_from_files()

    if not tokens_list:
        return []
    
    result: [TokenModel] = []
    for token in tokens_list:
        if token.symbol.lower() == string.lower() or token.name.lower() == string.lower():
            result.append(token)

    return result

def get_token_with(name: str) -> TokenModel:
    tokens_list: [TokenModel] = get_tokens_list_from_files()

    if not tokens_list:
        return None
    
    for token in tokens_list:
        if token.name.lower() == name.lower():
            return token