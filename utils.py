import os
from dotenv import load_dotenv
import json
from constants import MessageType
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
    cache_file.close()

    tokens = []
    for token in json_data['list']:
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

def check_if_user_added_to_cache(id):
    cache_file = open('cache_user_message.json', 'r')
    id = str(id)

    json_data = json.load(cache_file)
    try:
        existence = json_data[id]
        return True
    except:
        return False

def add_user_to_cache(id):
    cache_file = open('cache_user_message.json', 'r')
    id = str(id)

    json_data = json.load(cache_file)
    json_data[id] = {
        "predict": [],
        "info": []
    }
    print(json_data)
    cache_file.close()

    with open('cache_user_message.json', "w") as cache_file:
        json.dump(json_data, cache_file)
    

def add_user_message_to_cache(id, type: MessageType, message: [str]):
    cache_file = open('cache_user_message.json', 'r')
    json_data = json.load(cache_file)
    id = str(id)

    if type == MessageType.INFO:
        json_data[id]['info'] = message
    elif type == MessageType.PREDICT:
        json_data[id]['predict'] = message
    
    cache_file.close()

    with open('cache_user_message.json', "w") as cache_file:
        json.dump(json_data, cache_file)

def get_user_message_from_cache(id, type: MessageType):
    cache_file = open('cache_user_message.json', 'r')
    json_data = json.load(cache_file)
    id = str(id)

    if not json_data[id]:
        cache_file.close()
        add_user_to_cache(id)
        cache_file = open('cache_user_message.json', 'r')
        json_data = json.load(cache_file)
        cache_file.close()

    messages_cache = json_data[id]

    if type == MessageType.INFO:
        cache_file.close()
        return messages_cache['info']
    elif type == MessageType.PREDICT:
        cache_file.close()
        return messages_cache['predict']

def clear_message_cache_for_user(id):
    cache_file = open('cache_user_message.json', 'r')
    json_data = json.load(cache_file)
    id = str(id)

    json_data[id]['info'] = []
    json_data[id]['predict'] = []
    
    cache_file.close()

    with open('cache_user_message.json', "w") as cache_file:
        json.dump(json_data, cache_file)

def get_all_cache():
    cache_file = open('cache_user_message.json', 'r')
    json_data = json.load(cache_file)
    print(json.dumps(json_data, indent=4))
