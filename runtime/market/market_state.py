from datetime import datetime


class MarketState:

    def __init__(self):
        self.market_data = {}

    def get_session(self):
        hour = datetime.utcnow().hour

        if 0 <= hour < 6:
            return "TOKYO"
        elif 6 <= hour < 13:
            return "LONDON"
        elif 13 <= hour < 22:
            return "NEWYORK"
        return "DEAD_ZONE"

    def get_spread(self, session):
        base = 0.8

        if session == "TOKYO":
            return round(base + 0.4, 2)
        if session == "LONDON":
            return round(base + 0.2, 2)
        if session == "NEWYORK":
            return round(base + 0.3, 2)
        return 3.0

    def calculate_volatility(self):
        highs = [101, 103, 104, 106, 105]
        lows = [99, 100, 101, 102, 101]

        trs = [h - l for h, l in zip(highs, lows)]
        atr = sum(trs) / len(trs)

        return round(atr / 10, 2)

    def get_regime(self, volatility):
        if volatility > 1.2:
            return "HIGH_VOLATILITY"
        if volatility > 0.7:
            return "TREND"
        return "RANGE"

    def build(self):
        session = self.get_session()
        spread = self.get_spread(session)
        volatility = self.calculate_volatility()
        regime = self.get_regime(volatility)

        self.market_data = {
            "direction": "RANGE",
            "confidence": 0.7,
            "spread": spread,
            "volatility": volatility,
            "drawdown": 0.0,
            "loss_streak": 0,
            "session": session,
            "regime": regime
        }

        return self.market_data


# 笘・engine莠呈鋤逕ｨ・医％繧碁㍾隕・ｼ・
def get_market_data():
    return MarketState().build()


