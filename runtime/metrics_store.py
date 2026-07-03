import time


class MetricsStore:

    def __init__(self):
        self.trades = []

        self.wins = 0
        self.losses = 0

        # 学習データ
        self.confidences = []
        self.volatilities = []
        self.diffs = []

    # =========================
    # トレード記録（ALL）
    # =========================
    def log_trade(self, result, market_data=None, signal=None):

        r = result.get("result", {})
        retcode = r.get("retcode")

        self.trades.append(r)

        # 勝敗判定（簡易）
        is_win = retcode == 10009

        if is_win:
            self.wins += 1
        else:
            self.losses += 1

        # =========================
        # 学習データ収集
        # =========================
        if signal:
            self.confidences.append(signal.get("confidence", 0))

        if market_data:
            self.volatilities.append(market_data.get("volatility", 0))
            self.diffs.append(market_data.get("ma_short", 0) - market_data.get("ma_long", 0))

    # =========================
    # 勝率
    # =========================
    def win_rate(self):
        total = self.wins + self.losses
        if total == 0:
            return 0.0
        return self.wins / total

    # =========================
    # 平均パラメータ（本番最適化用）
    # =========================
    def get_optimal_params(self):

        if not self.trades:
            return None

        return {
            "avg_confidence": sum(self.confidences) / max(len(self.confidences), 1),
            "avg_volatility": sum(self.volatilities) / max(len(self.volatilities), 1),
            "avg_diff": sum(self.diffs) / max(len(self.diffs), 1),
        }