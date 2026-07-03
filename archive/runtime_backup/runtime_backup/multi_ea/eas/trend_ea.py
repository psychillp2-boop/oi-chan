class TrendEA:

    def generate_signal(self, market_data):

        return {
            "action": "buy" if market_data.get("trend") == "up" else "sell",
            "confidence": 0.6
        }