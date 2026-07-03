import numpy as np

def get_market_data(closes):

    ma_short = np.mean(closes[-5:])
    ma_long = np.mean(closes[-20:])

    diff = (ma_short - ma_long) / ma_long

    # =========================
    # TREND FILTER（強化）
    # =========================
    if diff > 0.00008:
        trend = "up"
    elif diff < -0.00008:
        trend = "down"
    else:
        trend = "sideways"

    # =========================
    # VOLATILITY（安定化）
    # =========================
    volatility = np.std(closes[-20:]) / ma_long

    return {
        "trend": trend,
        "volatility": float(volatility),
        "ma_short": float(ma_short),
        "ma_long": float(ma_long),
    }