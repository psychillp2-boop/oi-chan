import time


class FakeMT5Client:
    """
    MT5の代替（強制障害テスト用）
    """
    def __init__(self):
        self.alive = True

    def account_info(self):
        if not self.alive:
            raise Exception("MT5 DISCONNECTED")
        return {"balance": 1000}

    def initialize(self):
        print("[FAKE MT5] reconnect")
        self.alive = True
        return True

    def shutdown(self):
        print("[FAKE MT5] shutdown")
        self.alive = False


def test_healing(runtime, mt5):
    print("=== START TEST ===")

    # ① 正常状態
    print("[STEP 1] normal state")
    runtime.cycle({"test": 1})

    time.sleep(1)

    # ② 強制切断
    print("[STEP 2] FORCE DISCONNECT")
    mt5.shutdown()

    # ③ 何回か回す（復旧確認）
    for i in range(5):
        print(f"[STEP 3] cycle {i+1}")
        runtime.cycle({"test": 2})
        time.sleep(1)

    print("=== END TEST ===")