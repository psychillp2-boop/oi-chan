class ATRRegimeAI:

    def __init__(self, atr_threshold=0.4):
        self.atr_threshold = atr_threshold

    # =========================
    # 相場判定
    # =========================
    def detect(self, state):

        atr = state.get("atr", 0.2)
        trend = state.get("trend_strength", 0.5)

        # =========================
        # 強トレンド
        # =========================
        if atr > self.atr_threshold and trend > 0.6:
            return "TREND"

        # =========================
        # 弱トレンド
        # =========================
        if atr < self.atr_threshold and trend < 0.4:
            return "RANGE"

        # =========================
        # 中間（安全ゾーン）
        # =========================
        return "NEUTRAL"