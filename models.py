import json
from dataclasses import dataclass

@dataclass
class TokenModel:
    id: str
    symbol: str
    name: str

@dataclass
class ROI:
    times: float
    currency: str
    percentage: float

@dataclass
class MarketModel:
    id: str
    symbol: str
    name: str
    image: str
    current_price: float
    market_cap: float
    market_cap_rank: float
    fully_diluted_valuation: float
    total_volume: float
    high_24h: float
    low_24h: float
    price_change_24h: float
    price_change_percentage_24h: float
    market_cap_change_24h: float
    market_cap_change_percentage_24h: float
    circulating_supply: float
    total_supply: float
    max_supply: float
    ath: float
    ath_change_percentage: float
    ath_date: str
    atl: float
    atl_change_percentage: float
    atl_date: str
    roi: ROI
    last_updated: str

# data = '{"id": "01coin", "symbol": "zoc", "name": "01coin"}'
# json_data = json.loads(data)

# x = TokenModel(**json_data)
# print(x)