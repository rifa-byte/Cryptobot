# exchange_client.py
import ccxt
import config

def get_exchange():
    exchange_class = getattr(ccxt, config.EXCHANGE_ID)
    exchange = exchange_class({"enableRateLimit": True})
    return exchange

def fetch_candles(exchange, symbol, timeframe="15m", limit=100):
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
