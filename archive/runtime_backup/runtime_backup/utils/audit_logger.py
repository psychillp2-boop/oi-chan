import csv
import os
from datetime import datetime


class CSVLogger:

    def __init__(self, filename="log.csv"):
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["time", "event", "data"])

    def log(self, event, data):
        with open(self.filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),
                event,
                str(data)
            ])

    def log_system(self, message):
        self.log("SYSTEM", message)

    def log_error(self, message):
        self.log("ERROR", message)

    def log_trade(self, mode, signal, lot, price=None):
        self.log("TRADE", {
            "mode": mode,
            "signal": signal,
            "lot": lot,
            "price": price
        })


