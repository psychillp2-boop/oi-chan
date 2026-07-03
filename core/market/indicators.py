import numpy as np


class Indicators:

    # =========================
    # 移動平均
    # =========================
    def sma(self, prices, period=14):
        if len(prices) < period:
            return None
        return np.mean(prices[-period:])

    # =========================
    # RSI
    # =========================
    def rsi(self, prices, period=14):

        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(-period, -1):
            diff = prices[i] - prices[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(diff))

        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # =========================
    # トレンド判定
    # =========================
    def trend(self, prices):

        ma_short = self.sma(prices, 10)
        ma_long = self.sma(prices, 30)
        rsi = self.rsi(prices, 14)

        if ma_short is None or ma_long is None or rsi is None:
            return "neutral"

        # -------------------------
        # 強い上昇トレンド
        # -------------------------
        if ma_short > ma_long and rsi > 55:
            return "up"

        # -------------------------
        # 強い下降トレンド
        # -------------------------
        if ma_short < ma_long and rsi < 45:
            return "down"

        # -------------------------
        # レンジ
        # -------------------------
        return "sideways"