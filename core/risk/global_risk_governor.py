class GlobalRiskGovernor:

    def __init__(self):
        self.max_drawdown = 0.2
        self.peak = 10000

    def check(self, equity, peak_equity):

        drawdown = (peak_equity - equity) / peak_equity

        if drawdown > self.max_drawdown:
            return False

        return True