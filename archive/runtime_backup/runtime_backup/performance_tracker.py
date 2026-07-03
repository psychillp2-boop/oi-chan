class PerformanceTracker:

    def __init__(self):
        self.stats = {
            "USDJPY": {"win": 0, "loss": 0},
            "EURUSD": {"win": 0, "loss": 0},
            "GBPJPY": {"win": 0, "loss": 0}
        }

    def update(self, symbol, success: bool):

        if success:
            self.stats[symbol]["win"] += 1
        else:
            self.stats[symbol]["loss"] += 1

    def get_winrate(self, symbol):

        s = self.stats[symbol]
        total = s["win"] + s["loss"]

        if total == 0:
            return 0.5

        return s["win"] / total

    def get_all(self):

        return {
            k: self.get_winrate(k)
            for k in self.stats.keys()
        }