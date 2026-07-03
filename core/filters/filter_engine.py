import time


class FilterEngine:
    def __init__(self):
        self.last_signal = None
        self.last_signal_count = 0
        self.last_trade_side = None
        self.last_trade_time = 0
        self.cooldown_sec = 5
        self.last_reason = None

        # 📊 追加：分析用
        self.reason_count = {}
        self.confidence_history = []

    # =========================
    # 主判定
    # =========================
    def allow(self, signal, confidence, now):

        signal_type = signal.get("action", "HOLD").upper()

        # 📊 confidenceログ（追加）
        self.log_confidence(confidence)

        # LOW CONFIDENCE
        if confidence < 0.2:
            self.last_reason = "LOW_CONFIDENCE"
            self.log_reason(self.last_reason)
            return False

        # SIGNAL HOLD
        if signal_type == "HOLD":
            self.last_reason = "SIGNAL_HOLD"
            self.log_reason(self.last_reason)
            return False

        # SIGNAL REPEAT
        if signal_type == self.last_signal:
            self.last_signal_count += 1
        else:
            self.last_signal = signal_type
            self.last_signal_count = 1

        if self.last_signal_count >= 3:
            self.last_reason = "SIGNAL_REPEAT"
            self.log_reason(self.last_reason)
            return False

        # COOLDOWN
        if now - self.last_trade_time < self.cooldown_sec:
            self.last_reason = "COOLDOWN"
            self.log_reason(self.last_reason)
            return False

        # SAME DIRECTION
        if signal_type == self.last_trade_side:
            self.last_reason = "SAME_DIRECTION"
            self.log_reason(self.last_reason)
            return False

        self.last_reason = "ALLOW"
        self.log_reason(self.last_reason)
        return True

    # =========================
    # トレード記録
    # =========================
    def on_trade(self, signal_type, now):
        self.last_trade_side = signal_type
        self.last_trade_time = now

    # =========================
    # 理由カウント
    # =========================
    def log_reason(self, reason):
        if reason is None:
            return
        self.reason_count[reason] = self.reason_count.get(reason, 0) + 1

    # =========================
    # confidence履歴
    # =========================
    def log_confidence(self, confidence):
        self.confidence_history.append(confidence)