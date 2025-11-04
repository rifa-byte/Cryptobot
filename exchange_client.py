# exchange_client.py (OKX version)
import ccxt
import os

def get_exchange():
    exchange = ccxt.okx({
        "apiKey": os.getenv("OKX_API_KEY"),
        "secret": os.getenv("OKX_SECRET"),
        "password": os.getenv("OKX_PASSWORD"),
        "enableRateLimit": True,
    })
    # OKX demo mode
    # exchange.set_sandbox_mode(True)  # uncomment if you create a demo key
    return exchange
