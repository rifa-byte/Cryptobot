# main.py — runs the whole bot
import time
import config
from exchange_client import get_exchange, fetch_candles
from risk_engine import RiskEngine
from strategies.breakdown_short_m15 import BreakdownShortM15
from notify_telegram import alert

def main():
    exchange = get_exchange()
    risk = RiskEngine(starting_equity=1000)
    strategies = [BreakdownShortM15()]

    while True:
        market_data = {}
        for sym in config.SYMBOLS:
            candles = fetch_candles(exchange, sym, config.TIMEFRAME, limit=60)
            market_data[sym] = candles
            time.sleep(0.2)

        for strat in strategies:
            signals = strat.run(market_data)
            for sig in signals:
                size_pct = risk.size_for_signal(sig)
                msg = (f"[{strat.name}] {sig.side.upper()} {sig.symbol}\n"
                       f"TP={sig.tp}\nSL={sig.stop}\nSize%={size_pct*100:.1f}")
                print(msg)
                alert(msg)   # 🔔 sends Telegram alert
        time.sleep(60)

if __name__ == "__main__":
    main()
