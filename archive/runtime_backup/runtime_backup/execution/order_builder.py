import numpy as np


class OrderBuilder:

    def build(self, decision, risk, state):

        symbol = "USDJPY"
        signal = decision.get("signal", "buy")

        price = float(state.get("price", 0))

        sl = risk.get("sl", 0)
        tp = risk.get("tp", 0)

        # =========================
        # 型統一（超重要）
        # =========================
        sl = float(sl) if sl is not None else 0.0
        tp = float(tp) if tp is not None else 0.0

        lot = risk.get("lot", 0.01)
        lot = float(lot)

        # =========================
        # 正規化（安全）
        # =========================
        if signal == "buy":
            order_type = "buy"
        else:
            order_type = "sell"

        order = {
            "symbol": symbol,
            "type": order_type,
            "lot": lot,
            "sl": sl,
            "tp": tp,
            "price": price
        }

        return order