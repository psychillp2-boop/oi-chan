class RegimeFilter:
    def check(self, price):
        p = price["price"]

        if abs(p - 1.1000) < 0.002:
            return "RANGE"

        return "TREND"