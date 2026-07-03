import datetime


class PerformanceTracker:

    def __init__(self):
        self.trades = []
        self.balance_start = 0
        self.peak_balance = 0
        self.max_drawdown = 0
        self.loss_streak = 0

    # =========================
    # 初期資金設定
    # =========================
    def set_balance(self, balance):
        self.balance_start = balance
        self.peak_balance = balance

    # =========================
    # トレード記録
    # =========================
    def add_trade(self, result):

        self.trades.append(result)

        profit = result.get("profit", 0)

        # =========================
        # 連敗カウント
        # =========================
        if profit < 0:
            self.loss_streak += 1
        else:
            self.loss_streak = 0

        # =========================
        # ドローダウン計算
        # =========================
        if profit + self.peak_balance > self.peak_balance:
            self.peak_balance = profit + self.peak_balance

        current_balance = self.peak_balance + sum(t.get("profit", 0) for t in self.trades)

        dd = self.peak_balance - current_balance

        if dd > self.max_drawdown:
            self.max_drawdown = dd

        print(f"[TRACKER] profit={profit} loss_streak={self.loss_streak} DD={self.max_drawdown}")

    # =========================
    # 状態取得
    # =========================
    def get_stats(self):

        total_profit = sum(t.get("profit", 0) for t in self.trades)
        win_rate = 0

        wins = len([t for t in self.trades if t.get("profit", 0) > 0])

        if len(self.trades) > 0:
            win_rate = wins / len(self.trades) * 100

        return {
            "total_trades": len(self.trades),
            "total_profit": total_profit,
            "win_rate": win_rate,
            "loss_streak": self.loss_streak,
            "max_drawdown": self.max_drawdown
        }