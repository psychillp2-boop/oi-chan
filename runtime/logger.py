import json
import os
from datetime import datetime


class Logger:

    def __init__(self, path="logs/trade_log.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

    def log(self, data: dict):

        record = {
            "time": datetime.utcnow().isoformat(),
            "data": data
        }

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")