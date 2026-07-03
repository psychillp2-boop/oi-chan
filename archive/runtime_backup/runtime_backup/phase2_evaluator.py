from runtime.metrics_store import get_metrics


class Phase2Evaluator:

    def evaluate(self):

        m = get_metrics()

        return {
            "runtime_sec": m["runtime_sec"],
            "loops": m["loops"],
            "errors": m["errors"],
            "phase2_pass": (
                m["loops"] > 300 and
                m["errors"] < 5 and
                m["runtime_sec"] > 600
            )
        }