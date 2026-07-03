def calc_lot(balance: float, risk_ratio: float = 0.01) -> float:
    lot = (balance * risk_ratio) / 10000
    return round(max(lot, 0.01), 2)