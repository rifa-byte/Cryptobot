# strategies/breakdown_short_m15.py
from strategy_base import Strategy, Signal

LOOKBACK = 20
VOLUME_MULT = 1.5

class BreakdownShortM15(Strategy):
    name = "breakdown_short_m15"

    def run(self, market_data):
        signals = []
        for symbol, candles in market_data.items():
            if len(candles) < LOOKBACK + 2:
                continue
            last = candles[-2]
            prev = candles[-2-LOOKBACK:-2]
            recent_low = min(c[3] for c in prev)
            avg_vol = sum(c[5] for c in prev) / len(prev)
            last_close = last[4]
            last_vol = last[5]
            if last_close < recent_low and last_vol > VOLUME_MULT * avg_vol:
                stop = last[2]
                entry = last_close
                risk = stop - entry if stop > entry else 0.0001
                tp = entry - risk
                signals.append(Signal(symbol, "sell", 1.0, stop, tp))
        return signals
