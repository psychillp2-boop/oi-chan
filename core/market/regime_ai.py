class MarketRegimeAI:

    def __init__(self):
        pass

    # =========================
    # 相場判定
    # =========================
    def detect(self, state):

        price = state.get("price", 0)
        high = state.get("high", price)
        low = state.get("low", price)

        volatility = abs(high - low)

        # 超シンプル判定
        if volatility > 0.5:
            return "TREND"
        else:
            return "RANGE"