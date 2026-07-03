import json
from collections import defaultdict


LOG_PATH = "logs/trade_log.jsonl"


class Phase1Judge:

    def __init__(self):

        self.stats = defaultdict(int)

    # =========================
    # LOG READ
    # =========================
    def load_logs(self):

        logs = []

        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                for line in f:
                    logs.append(json.loads(line.strip()))
        except FileNotFoundError:
            print("❌ log file not found")
            return []

        return logs

    # =========================
    # ANALYZE
    # =========================
    def analyze(self, logs):

        for entry in logs:

            data = entry.get("data", {})
            event = data.get("event")

            # INIT
            if event == "INIT_OK":
                self.stats["init_ok"] += 1
            if event == "INIT_FAIL":
                self.stats["init_fail"] += 1

            # ORDER
            if event == "ORDER":
                self.stats["order_total"] += 1

                if data.get("success"):
                    self.stats["order_success"] += 1
                else:
                    self.stats["order_fail"] += 1

            # SAFETY
            if event == "BLOCK":
                self.stats["blocked"] += 1

            # RECOVERY
            if event == "RECOVERY_OK":
                self.stats["recovery_ok"] += 1

            if event == "RECOVERY_FAIL":
                self.stats["recovery_fail"] += 1

    # =========================
    # JUDGE
    # =========================
    def judge(self):

        total = self.stats["order_total"]
        success = self.stats["order_success"]

        if total == 0:
            return {
                "status": "FAIL",
                "reason": "NO_ORDERS"
            }

        success_rate = success / total

        # ===== フェーズ1基準 =====
        result = {
            "total_orders": total,
            "success": success,
            "fail": self.stats["order_fail"],
            "success_rate": round(success_rate, 3),
            "blocked": self.stats["blocked"],
            "recovery_ok": self.stats["recovery_ok"],
            "recovery_fail": self.stats["recovery_fail"],
        }

        # 合否判定
        if (
            success_rate >= 0.8 and
            self.stats["init_fail"] == 0 and
            self.stats["recovery_fail"] == 0
        ):
            result["phase1"] = "PASS"
        else:
            result["phase1"] = "FAIL"

        return result


# =========================
# RUN
# =========================
if __name__ == "__main__":

    judge = Phase1Judge()

    logs = judge.load_logs()

    judge.analyze(logs)

    result = judge.judge()

    print("\n===== PHASE1 RESULT =====")
    for k, v in result.items():
        print(k, ":", v)