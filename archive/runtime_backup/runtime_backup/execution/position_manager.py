class PositionManager:

    def open(self, strategy, lot):
        return {
            "strategy": strategy,
            "lot": lot,
            "status": "OPENED"
        }