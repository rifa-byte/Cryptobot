# main.py — OKX bot with PAPER/LIVE announcement
import time
import config
from exchange_client import get_exchange, fetch_candles
from risk_engine import RiskEngine
from strategies.breakdown_short_m15 import BreakdownShortM15
from notify_telegram import alert

exchange = get_exchange()
risk = RiskEngine(starting_equity=36)  # 50 SGD ≈ 36 USD
strategies = [BreakdownShortM15()]

# --- SETTINGS YOU CHANGE ---
MAX_BALANCE_USD = 36          # your budget (~$50 SGD)
RISK_PER_TRADE = 0.02         # 2% of your budget per trade
PAPER_MODE = True             # 🔁 TODAY: keep this True; tomorrow set to False
# ----------------------------

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

        if PAPER_MODE:
            # just simulate
            alert(f"📊 PAPER: {side.upper()} {symbol} ≈ ${trade_value:.2f} @ ${price:.2f}")
            print(f"[PAPER TRADE] {side.upper()} {symbol} amount={amount} (${trade_value:.2f})")
        else:
            # real order
            alert(f"⚠️ LIVE ORDER: {side.upper()} {symbol} ≈ ${trade_value:.2f} @ ${price:.2f}")
            if side == "buy":
                exchange.create_market_buy_order(symbol, amount)
            elif side == "sell":
                exchange.create_market_sell_order(symbol, amount)
            alert(f"✅ LIVE {side.upper()} executed for {symbol} (${trade_value:.2f})")

    except Exception as e:
        alert(f"❌ Trade failed for {signal.symbol}: {e}")
        print("Trade error:", e)

def main():
    # ✅ Safety announcement on startup
    if PAPER_MODE:
        alert("🧾 OKX Bot started in PAPER MODE — no real orders will be sent.")
    else:
        alert("⚠️ OKX Bot started in LIVE MODE — REAL orders will be executed. Double-check balances.")

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
                    # basic alert for the signal
                    alert(f"[{strat.name}] {sig.side.upper()} {sig.symbol}")
                    place_trade(sig)

            time.sleep(60)

        except Exception as e:
            alert(f"⚠️ Error in loop: {e}")
            print("Main loop error:", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
