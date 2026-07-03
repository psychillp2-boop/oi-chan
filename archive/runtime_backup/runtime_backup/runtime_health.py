import MetaTrader5 as mt5
import time


class RuntimeHealth:

    def __init__(self):

        self.fail_count = 0
        self.max_fail = 3

    # =========================
    # 状態チェック
    # =========================
    def check(self):

        issues = []

        # MT5接続
        if not mt5.initialize():
            issues.append("MT5_DISCONNECTED")

        # tickチェック
        tick = mt5.symbol_info_tick("USDJPY")
        if tick is None:
            issues.append("NO_TICK")

        return issues

    # =========================
    # 軽い修復
    # =========================
    def recover(self, issues):

        for i in issues:

            if i == "MT5_DISCONNECTED":

                self.fail_count += 1

                if self.fail_count >= self.max_fail:
                    return "STOP_SYSTEM"

                mt5.shutdown()
                time.sleep(1)
                mt5.initialize()

            if i == "NO_TICK":
                time.sleep(1)

        return "OK"