import numpy as np
import time


class RiskGovernorV2:

    def __init__(self):

        self.daily_pnl = []
        self.consecutive_losses = 0
        self.last_reset = time.time()

        # リスク上限
        self.max_drawdown = 0.05
        self.max_daily_loss = 0.02
        self.max_positions = 2

        # VaR設定（95%）
        self.var_threshold = 0.03

    # =========================
    # トレード許可判定
    # =========================
    def allow_trade(self, account, context, portfolio_state):

        self._reset_daily()

        # ① ドローダウン
        if account.get("equity_drop", 0) >= self.max_drawdown:
            print("[RISK V2] DRAWDOWN BLOCK")
            return False

        # ② 日次損失
        if self._daily_loss() >= self.max_daily_loss:
            print("[RISK V2] DAILY LOSS BLOCK")
            return False

        # ③ 連敗制御
        if self.consecutive_losses >= 3:
            print("[RISK V2] LOSS STREAK BLOCK")
            return False

        # ④ ポジション制御
        if context.get("positions", 0) >= self.max_positions:
            print("[RISK V2] POSITION LIMIT BLOCK")
            return False

        # ⑤ VaR（統計リスク）
        if self._calc_var(portfolio_state) > self.var_threshold:
            print("[RISK V2] VaR BLOCK")
            return False

        # ⑥ 相関リスク
        if self._correlation_risk(portfolio_state) > 0.7:
            print("[RISK V2] CORRELATION BLOCK")
            return False

        return True

    # =========================
    # 結果更新
    # =========================
    def update_result(self, success: bool, pnl: float):

        self.daily_pnl.append(pnl)

        if success:
            self.consecutive_losses = 0
        else:
            self.consecutive_losses += 1

    # =========================
    # 日次損失
    # =========================
    def _daily_loss(self):

        if not self.daily_pnl:
            return 0.0

        return abs(sum([x for x in self.daily_pnl if x < 0]))

    # =========================
    # VaR計算（簡易）
    # =========================
    def _calc_var(self, portfolio_state):

        returns = portfolio_state.get("returns", [0])

        if len(returns) < 10:
            return 0.0

        return np.percentile(returns, 5) * -1  # 95% VaR

    # =========================
    # 相関リスク
    # =========================
    def _correlation_risk(self, portfolio_state):

        corr_matrix = portfolio_state.get("correlation", [[0]])

        if not corr_matrix:
            return 0.0

        # 最大相関
        return np.max(corr_matrix)

    # =========================
    # リセット
    # =========================
    def _reset_daily(self):

        now = time.time()

        if now - self.last_reset >= 86400:
            print("[RISK V2] DAILY RESET")
            self.daily_pnl = []
            self.consecutive_losses = 0
            self.last_reset = now