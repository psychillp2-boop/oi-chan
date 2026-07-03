class Context:
    def __init__(self):
        # ===== CONTROL =====
        self.stop = False
        self.loop_count = 0

        # ===== MARKET =====
        self.market = None
        self.signal = None

        # ===== RISK（ここが重要）=====
        self.drawdown = 0.0
        self.loss_streak = 0

        # ===== STATE =====
        self.session = None
        self.regime = None


