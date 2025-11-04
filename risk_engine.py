# risk_engine.py
import config

class RiskEngine:
    def __init__(self, starting_equity):
        self.peak_equity = starting_equity
        self.current_equity = starting_equity

    def update_equity(self, new_equity):
        self.current_equity = new_equity
        if new_equity > self.peak_equity:
            self.peak_equity = new_equity

    def current_dd(self):
        return 1 - (self.current_equity / self.peak_equity)

    def size_for_signal(self, signal):
        base_pct = 0.01
        dd = self.current_dd()
        if dd > 0.2:
            base_pct *= 0.5
        return base_pct
