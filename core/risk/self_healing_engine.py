import time
import MetaTrader5 as mt5


class SelfHealingEngine:

    def __init__(self):
        self.last_reconnect_time = 0
        self.reconnect_cooldown = 10  # 連続リカバリ防止

        self.mt5_error_count = 0

    # =========================
    # MT5接続監視のみ
    # =========================
    def check_health(self, positions, last_trade_time):
        # signalや価格は見ない（重要）
        # ここではMT5状態だけを見る

        if not mt5.initialize():
            return self.recover_mt5()

        return True

    # =========================
    # MT5リカバリ
    # =========================
    def recover_mt5(self):

        now = time.time()

        # クールダウン（連打防止）
        if now - self.last_reconnect_time < self.reconnect_cooldown:
            return False

        self.last_reconnect_time = now

        try:
            print("[HEAL] MT5 recovering...")

            mt5.shutdown()
            time.sleep(1)

            if mt5.initialize():
                print("[HEAL] MT5 reconnected")
                self.mt5_error_count = 0
                return True

            self.mt5_error_count += 1
            return False

        except Exception as e:
            self.mt5_error_count += 1
            print("[HEAL][ERROR]", e)
            return False