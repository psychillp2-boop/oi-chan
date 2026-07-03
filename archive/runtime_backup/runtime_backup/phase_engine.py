from runtime.phase2_evaluator import Phase2Evaluator
from runtime.phase3_score import Phase3Score
from runtime.phase1_judge import Phase1Judge


class PhaseEngine:

    def __init__(self):
        self.phase2 = Phase2Evaluator()
        self.phase3 = Phase3Score()
        self.phase1 = Phase1Judge()

    # ===================================
    # Phase1
    # ===================================
    def check_phase1(self):

        logs = self.phase1.load_logs()
        self.phase1.analyze(logs)

        return self.phase1.judge()

    # ===================================
    # Phase2
    # ===================================
    def check_phase2(self):

        return self.phase2.evaluate()

    # ===================================
    # Phase3
    # ===================================
    def check_phase3(self):

        return self.phase3.evaluate()

    # ===================================
    # ALL
    # ===================================
    def run_all(self):

        print("\n🚀 ===== PHASE ENGINE START =====")

        p2 = self.check_phase2()
        p3 = self.check_phase3()
        p1 = self.check_phase1()

        print("\n📊 ===== RESULTS =====")
        print("Phase2 :", p2)
        print("Phase3 :", p3)
        print("Phase1 :", p1)

        phase1_ok = p1.get("phase1") == "PASS"
        phase2_ok = p2.get("phase2_pass", False)
        phase3_ok = p3.get("pass", False)

        print()

        if phase1_ok and phase2_ok and phase3_ok:

            print("🎉 FINAL RESULT : PASS")
            print("🚀 READY FOR PHASE 3")

        else:

            print("❌ FINAL RESULT : FAIL")
            print("➡ STAY PHASE 2")


if __name__ == "__main__":

    engine = PhaseEngine()
    engine.run_all()