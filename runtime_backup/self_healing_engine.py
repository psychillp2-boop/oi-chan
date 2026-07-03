import MetaTrader5 as mt5
import time


class SelfHealingEngine:

    def __init__(self, broker):
        self.broker = broker
        self.retry_count = {}

    # =========================
    # ENTRY POINT
    # =========================
    def handle(self, error_type, context=None):

        print(f"[HEAL] {error_type}")

        # -------------------------
        # ① MT5切断
        # -------------------------
        if error_type == "MT5_DISCONNECTED":
            return self._reconnect_mt5()

        # -------------------------
        # ② Tickエラー
        # -------------------------
        if error_type == "NO_TICK":
            return self._retry_symbol(context)

        # -------------------------
        # ③ 注文エラー
        # -------------------------
        if error_type == "ORDER_FAILED":
            return self._retry_order(context)

        # -------------------------
        # ④ 不明エラー
        # -------------------------
        return False

    # =========================
    # MT5再接続
    # =========================
    def _reconnect_mt5(self):

        print("[HEAL] reconnect MT5...")

        mt5.shutdown()
        time.sleep(2)

        if mt5.initialize():
            print("[HEAL] MT5 RECONNECTED")
            return True

        print("[HEAL] FAILED")
        return False

    # =========================
    # シンボル再取得
    # =========================
    def _retry_symbol(self, symbol):

        if not symbol:
            return False

        print(f"[HEAL] retry symbol {symbol}")

        return mt5.symbol_select(symbol, True)

    # =========================
    # 注文リトライ（1回だけ）
    # =========================
    def _retry_order(self, order):

        key = "order_retry"

        count = self.retry_count.get(key, 0)

        if count >= 1:
            print("[HEAL] retry limit reached")
            return False

        self.retry_count[key] = count + 1

        print("[HEAL] retry order once")

        try:
            return self.broker.send(order)
        except Exception as e:
            print("[HEAL ERROR]", e)
            return False