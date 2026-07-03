class PositionSizer:

    def __init__(self):
        self.min_lot = 0.01
        self.max_lot = 1.0

    def calc_lot(self, balance, risk, sl_pips, atr=None, drawdown=0):

        # 基本リスク額
        risk_amount = balance * risk

        # SLベース損失計算
        pip_value = 1000
        lot = risk_amount / max(sl_pips * pip_value, 1)

        # ボラ調整（あれば）
        if atr:
            lot *= 1 / max(atr, 0.0001)

        # ドローダウン制御
        if drawdown > 0.1:
            lot *= 0.5

        # 制限
        lot = max(self.min_lot, min(lot, self.max_lot))

        return round(lot, 2)