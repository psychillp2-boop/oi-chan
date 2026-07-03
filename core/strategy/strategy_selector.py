class StrategySelector:

    def select(self, regime):

        if regime == "TREND":
            return "trend_follow"

        if regime == "RANGE":
            return "mean_reversion"

        return "standby"