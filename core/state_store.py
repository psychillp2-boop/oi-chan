import MetaTrader5 as mt5


class StateStore:

    def __init__(self, symbol="USDJPY", timeframe=mt5.TIMEFRAME_M1):
        self.symbol = symbol
        self.timeframe = timeframe

    def get_state(self):

        rates = mt5.copy_rates_from_pos(self.symbol, self.timeframe, 0, 50)

        if rates is None or len(rates) < 20:
            return self._empty_state()

        closes = [r[4] for r in rates]
        highs = [r[2] for r in rates]
        lows = [r[3] for r in rates]

        price = closes[-1]

        tr_list = []
        for i in range(1, len(rates)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            tr_list.append(tr)

        atr = sum(tr_list[-14:]) / 14 if len(tr_list) >= 14 else 0.2

        ma_fast = sum(closes[-5:]) / 5
        ma_slow = sum(closes[-20:]) / 20

        trend_strength = abs(ma_fast - ma_slow) / price if price != 0 else 0

        return {
            "price": price,
            "high": max(highs[-20:]),
            "low": min(lows[-20:]),
            "atr": atr,
            "trend_strength": trend_strength
        }

    def _empty_state(self):
        return {
            "price": 0,
            "high": 0,
            "low": 0,
            "atr": 0.2,
            "trend_strength": 0.5
        }