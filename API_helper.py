import requests, json
from types import SimpleNamespace
from utils import get_cg_token
from models import *

class APIHelper:
    _BASE_URL = 'https://api.coingecko.com/api/v3'
    _TOKEN = get_cg_token()

    # HEADERS
    _HEADERS = {
        'x-cg-demo-api-key': _TOKEN
    }

    # ENDPOINTS
    _LIST_ENDPOINT = '/coins/list'
    _MARKETS_ENDPOINT = '/coins/markets'

    def get_token_list(self) -> [TokenModel]:
        url = self._BASE_URL + self._LIST_ENDPOINT

        response = requests.get(url=url, headers=self._HEADERS)

        if response.status_code != 200:
            return []
        
        response_json = response.json()

        with open('coins_data.json', "w") as cache_file:
            json.dump(response_json, cache_file)

        coins = []
        for coin in response_json:
            coins.append(TokenModel(**coin))

        return coins
    
    def get_token_list_100(self) -> [TokenModel]:
        url = self._BASE_URL + self._MARKETS_ENDPOINT
        params = {
            'vs_currency': 'usd',
            'page': 1,
            'per_page': 100,
            'order': 'market_cap_desc'
        }

        response = requests.get(url=url, params=params, headers=self._HEADERS)

        if response.status_code != 200:
            print("Error")
            return []

        response_json = response.json()
        print(response_json)

        top_100 = []
        for coin in response_json:
            top_100.append(MarketModel(**coin))

        return top_100

    def get_price(self, token_id: str):
        url = self._BASE_URL + self._MARKETS_ENDPOINT
        params = {
            'vs_currency': 'usd',
            'ids': token_id
        }

        response = requests.get(url, params=params, headers=self._HEADERS)

        if response.status_code != 200:
            print("Error")
            return []

        response_json = response.json()
        print(type(response_json))

        if len(response_json) == 1:
            coin_market_data = MarketModel(**response_json[0])
            print(coin_market_data)
            return coin_market_data
        else:
            print('Something is not right, it return more than one data.')
            print(json.dumps(response_json, indent=4))
            return None

        

# api_helper = APIHelper()
# coins_list = api_helper.get_price(token_id='bitcoin')