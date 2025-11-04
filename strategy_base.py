# strategy_base.py
class Signal:
    def __init__(self, symbol, side, confidence=1.0, stop=None, tp=None):
        self.symbol = symbol
        self.side = side
        self.confidence = confidence
        self.stop = stop
        self.tp = tp

class Strategy:
    name = "base"
    def run(self, market_data):
        return []

