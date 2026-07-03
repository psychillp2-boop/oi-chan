from runtime.multi_ea.eas.trend_ea import TrendEA
from runtime.multi_ea.eas.mean_reversion_ea import MeanReversionEA
from runtime.multi_ea.eas.breakout_ea import BreakoutEA

from runtime.execution.order_throttle import OrderThrottle


class MultiEAEngine:

    def __init__(self, portfolio_manager, risk_engine, executor):

        self.portfolio = portfolio_manager
        self.risk = risk_engine
        self.executor = executor

        # =========================
        # EA登録
        # =========================
        self.ea_modules = {
            "trend": TrendEA(),
            "mean_reversion": MeanReversionEA(),
            "breakout": BreakoutEA()
        }

        # =========================
        # 発注制御（重要）
        # =========================
        self.throttle = OrderThrottle()

    # =========================
    # メイン実行
    # =========================
    def run(self, market_data):

        results = []

        symbol = market_data.get("symbol", "USDJPY")
        price = market_data.get("price", 0)

        for name, ea in self.ea_modules.items():

            # =========================
            # ① 発注制御（超重要）
            # =========================
            if not self.throttle.allow(name):
                continue

            # =========================
            # ② シグナル取得
            # =========================
            signal = ea.generate_signal(market_data)

            if not signal:
                continue

            action = signal.get("action", "hold")
            confidence = signal.get("confidence", 0.5)

            # =========================
            # ③ 資金配分
            # =========================
            capital = self.portfolio.get_allocation(name)

            # =========================
            # ④ ロット計算
            # =========================
            lot = self.risk.calc_lot(
                account_balance=capital,
                risk_score=confidence,
                atr=market_data.get("atr", 0.001)
            )

            # =========================
            # ⑤ ロット安全制限（重要）
            # =========================
            lot = min(max(lot, 0.01), 0.3)

            # =========================
            # ⑥ order生成
            # =========================
            order = {
                "symbol": symbol,
                "type": action,
                "lot": lot,
                "price": price,
                "ea": name
            }

            # =========================
            # ⑦ 実行
            # =========================
            try:
                result = self.executor.execute(order, market_data)
                results.append(result)

            except Exception as e:
                print(f"[EXEC ERROR] {name}: {e}")

        return results