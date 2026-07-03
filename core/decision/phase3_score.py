from runtime.metrics_store import get_metrics


class Phase3Score:

    def evaluate(self):

        m = get_metrics()

        score = 0

        if m["runtime_sec"] > 600:
            score += 1

        if m["loops"] > 300:
            score += 1

        if m["errors"] < 5:
            score += 1

        if m["orders"] > 5:
            score += 1

        fail_rate = m["fail_orders"] / (m["orders"] + 1)
        if fail_rate < 0.3:
            score += 1

        return {
            "score": score,
            "pass": score >= 4,
            "metrics": m
        }