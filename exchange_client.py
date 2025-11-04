# exchange_client.py — OKX paper trading mode
import ccxt
import os

def get_exchange():
    exchange = ccxt.okx({
        "apiKey": os.getenv("OKX_API_KEY"),
        "secret": os.getenv("OKX_SECRET"),
        "password": os.getenv("OKX_PASSWORD"),
        "enableRateLimit": True,
    })
    exchange.set_sandbox_mode(True)  # ✅ DEMO MODE (fake money)
    return exchange

def fetch_candles(exchange, symbol, timeframe="15m", limit=100):
    return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
