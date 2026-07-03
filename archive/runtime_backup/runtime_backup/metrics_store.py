import json
import os
import time

METRICS_FILE = "logs/runtime_metrics.json"

DEFAULT = {
    "loops": 0,
    "errors": 0,
    "orders": 0,
    "fail_orders": 0,
    "start_time": time.time()
}


def _load():

    if not os.path.exists(METRICS_FILE):
        return DEFAULT.copy()

    try:
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return DEFAULT.copy()


def _save(metrics):

    os.makedirs("logs", exist_ok=True)

    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)


def inc(key):

    metrics = _load()

    metrics[key] += 1

    _save(metrics)


def get_metrics():

    metrics = _load()

    metrics["runtime_sec"] = (
        time.time() - metrics["start_time"]
    )

    return metrics


def reset_metrics():

    _save(DEFAULT.copy())