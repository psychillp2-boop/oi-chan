import time
import MetaTrader5 as mt5


class MT5System:

    def __init__(self, symbol="USDJPY"):

        self.symbol = symbol

        # =========================
        # 状態管理
        # =========================
        self.last_ok_time = time.time()
        self.fail_count = 0
        self.status = "INIT"

        # =========================
        # ログ管理
        # =========================
        self.logs = []

        # MT5初期化
        try:
            mt5.initialize()
            self.status = "OK"
        except:
            self.status = "FAIL"

    # =================================================
    # ① 接続チェック
    # =================================================
    def check(self):

        terminal_ok = mt5.terminal_info() is not None
        tick_ok = mt5.symbol_info_tick(self.symbol) is not None

        if terminal_ok and tick_ok:

            self.last_ok_time = time.time()
            self.fail_count = 0
            self.status = "OK"
            return True

        else:

            self.fail_count += 1
            self.status = "FAIL"
            return False

    # =================================================
    # ② 異常判定
    # =================================================
    def is_unhealthy(self):

        if time.time() - self.last_ok_time > 30:
            return True

        if self.fail_count >= 5:
            return True

        return False

    # =================================================
    # ③ リカバリー
    # =================================================
    def recover(self):

        print("[MT5 SYSTEM] RECOVERY START")

        try:
            mt5.shutdown()
            time.sleep(2)

            for i in range(5):

                print(f"[MT5 SYSTEM] RECOVERY TRY ({i+1})")

                if mt5.initialize():
                    self.fail_count = 0
                    self.last_ok_time = time.time()
                    self.status = "OK"

                    print("[MT5 SYSTEM] RECOVERY SUCCESS")
                    return True

                time.sleep(1)

        except Exception as e:
            print("[MT5 SYSTEM] RECOVERY ERROR:", e)

        self.status = "FAIL"
        return False

    # =================================================
    # ④ ログ（engine互換）
    # =================================================
    def log_result(self, results):

        log = {
            "time": time.time(),
            "symbol": self.symbol,
            "status": self.status,
            "results": results
        }

        self.logs.append(log)

        print("\n[MT5 SYSTEM]")
        print("[STATUS]", self.status)
        print("[RESULTS]", len(results))

        return log

    # =================================================
    # ⑤ equity（将来用）
    # =================================================
    def get_equity(self):

        try:
            account = mt5.account_info()
            if account:
                return account.balance
        except:
            pass

        return 10000

    # =================================================
    # ⑥ 状態取得
    # =================================================
    def get_state(self):

        return {
            "status": self.status,
            "fail_count": self.fail_count,
            "alive": not self.is_unhealthy()
        }