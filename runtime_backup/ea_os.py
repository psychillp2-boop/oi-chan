import time
import MetaTrader5 as mt5

from phase2_diagnosis import run_all as phase2_run
from runtime.self_healing_engine import SelfHealingEngine


class EA_OS:

    def __init__(self, interval_sec=30):

        self.interval = interval_sec
        self.healer = SelfHealingEngine(broker=self)
        self.running = True

    # =========================
    # MAIN LOOP
    # =========================
    def run(self):

        print("[EA_OS] START")

        while self.running:

            # -------------------------
            # ① Phase2チェック
            # -------------------------
            phase2 = self._phase2_check()

            # -------------------------
            # ② MT5状態チェック
            # -------------------------
            mt5_status = self._check_mt5()

            # -------------------------
            # ③ 判定
            # -------------------------
            self._evaluate(phase2, mt5_status)

            time.sleep(self.interval)

    # =========================
    # Phase2
    # =========================
    def _phase2_check(self):

        try:
            return run_all()
        except Exception as e:
            return {"status": "CRASH", "error": str(e)}

    # =========================
    # MT5監視
    # =========================
    def _check_mt5(self):

        try:

            if not mt5.initialize():
                return {"status": "FAIL", "error": "INIT_FAIL"}

            acc = mt5.account_info()

            if acc is None:
                mt5.shutdown()
                return {"status": "FAIL", "error": "ACCOUNT_FAIL"}

            mt5.shutdown()

            return {
                "status": "OK",
                "balance": acc.balance
            }

        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    # =========================
    # 判定 + 修復
    # =========================
    def _evaluate(self, phase2, mt5_status):

        print("\n[EA_OS STATUS]")

        print("[PHASE2]", phase2)
        print("[MT5]", mt5_status)

        # -------------------------
        # Phase2異常
        # -------------------------
        if isinstance(phase2, dict):

            if phase2.get("status") in ["FAIL", "CRASH"]:
                print("🚨 PHASE2 FAILURE → HEAL")
                self.healer.handle("PHASE2_FAIL")

        # -------------------------
        # MT5異常
        # -------------------------
        if mt5_status.get("status") != "OK":
            print("🚨 MT5 FAILURE → HEAL")
            self.healer.handle("MT5_DISCONNECTED")

        print("[EA_OS] OK")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":

    os = EA_OS(interval_sec=20)
    os.run()