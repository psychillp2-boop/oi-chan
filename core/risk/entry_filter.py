import time


class EntryFilter:

    def __init__(self, cooldown_sec=30):
        self.last_signal = None
        self.last_time = 0
        self.cooldown_sec = cooldown_sec

    # =========================
    # エントリー制御
    # =========================
    def allow(self, signal):

        now = time.time()

        # =========================
        # クールダウン制御
        # =========================
        if now - self.last_time < self.cooldown_sec:
            return False, "COOLDOWN_ACTIVE"

        # =========================
        # 同一シグナル連打防止
        # =========================
        if signal == self.last_signal:
            return False, "DUPLICATE_SIGNAL"

        # OK更新
        self.last_signal = signal
        self.last_time = now

        return True, "OK"