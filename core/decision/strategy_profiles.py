class StrategyProfiles:

    def __init__(self):

        self.profiles = {
            "MASTER_OMEGA": {
                "bias": "TREND",
                "risk": 1.0,
                "aggressiveness": 0.7
            },

            "YEN_OMEGA": {
                "bias": "USDJPY_TREND",
                "risk": 0.8,
                "aggressiveness": 0.6
            },

            "CRITICAL_OMEGA": {
                "bias": "MEAN_REVERSION",
                "risk": 1.2,
                "aggressiveness": 0.9
            }
        }

    def get(self, ea_name):
        return self.profiles.get(
            ea_name,
            {
                "bias": "NEUTRAL",
                "risk": 1.0,
                "aggressiveness": 0.5
            }
        )


# 笘・engine莠呈鋤逕ｨ
def generate_signal(market):

    direction = market.get("direction")

    if direction == "TREND":
        return "BUY"
    elif direction == "RANGE":
        return None

    return None


