# main.py — OKX Paper Trading Mode
import time
import config
from exchange_client import get_exchange, fetch_candles
from risk_engine import RiskEngine
from strategies.breakdown_short_m15 import BreakdownShortM15
from notify_telegram import alert

exchange = get_exchange()
risk = RiskEngine(starting_equity=36)  # 50 SGD ≈ 36 USD
strategies = [BreakdownShortM15()]

# --- Settings ---
MAX_BALANCE_USD = 36
RISK_PER_TRADE = 0.02
PAPER_MODE = True  # ✅ True = no real trades

def get_usdt_price(symbol="BTC/USDT"):
    ticker = exchange.fetch_ticker(symbol)
    return ticker["last"]

def place_trade(signal):
    try:
        symbol = signal.symbol
        side = signal.side.lower()
        price = get_usdt_price(symbol)
        trade_value = MAX_BALANCE_USD * RISK_PER_TRADE
        amount = trade_value / price

        alert(f"📊 PAPER: {side.upper()} {symbol} (${trade_value:.2f}) @ ${price:.2f}")

        if not PAPER_MODE:
            if side == "buy":
                exchange.create_market_buy_order(symbol, amount)
            elif side == "sell":
                exchange.create_market_sell_order(symbol, amount)
            alert(f"✅ LIVE {side.upper()} executed for {symbol} (${trade_value:.2f})")
        else:
            print(f"[PAPER TRADE] {side.upper()} {symbol} - Amount {amount} (${trade_value:.2f})")

    except Exception as e:
        alert(f"❌ Trade failed: {e}")
        print("Trade error:", e)

def main():
    alert("🧾 OKX Bot started in PAPER MODE with $50 SGD budget (~$36 USD)")
    while True:
        try:
            market_data = {}
            for sym in config.SYMBOLS:
                candles = fetch_candles(exchange, sym, config.TIMEFRAME, limit=60)
                market_data[sym] = candles
                time.sleep(0.3)

            for strat in strategies:
                signals = strat.run(market_data)
                for sig in signals:
                    msg = f"[{strat.name}] {sig.side.upper()} {sig.symbol}"
                    print(msg)
                    alert(msg)
                    place_trade(sig)

            time.sleep(60)

        except Exception as e:
            alert(f"⚠️ Error in loop: {e}")
            print("Main loop error:", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
