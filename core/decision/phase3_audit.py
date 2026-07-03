from runtime.phase3_score import Phase3ScoreCalculator
import time


class Phase3Audit:

    def __init__(self):
        self.calc = Phase3ScoreCalculator()

    def evaluate(self):

        result = self.calc.calculate()

        print("\n🚀 ===== Phase3 Report =====")
        print("DETAIL:", result["score_detail"])
        print("TOTAL :", result["total_score"])
        print("RESULT:", result["phase3"])