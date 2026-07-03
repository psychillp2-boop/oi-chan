class PortfolioManager:

    def __init__(self):

        # EAごとの資金配分比率
        self.allocations = {
            "trend": 0.4,
            "mean_reversion": 0.3,
            "breakout": 0.3
        }

        self.total_equity = 10000

    # =========================
    # EAごとの資金割当
    # =========================
    def get_allocation(self, ea_name):

        return self.total_equity * self.allocations.get(ea_name, 0)

    # =========================
    # 全体リスク制御
    # =========================
    def update_equity(self, new_equity):

        self.total_equity = new_equity

    # =========================
    # リスク集中防止
    # =========================
    def max_exposure(self):

        return self.total_equity * 0.1  # 最大10%同時リスク