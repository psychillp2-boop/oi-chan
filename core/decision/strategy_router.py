import numpy as np

class StrategyState:
    last_action = None
    same_count = 0


def get_signal(market_data):

    trend = market_data.get("trend", "sideways")
    volatility = market_data.get("volatility", 0)
    ma_short = market_data.get("ma_short", 0)
    ma_long = market_data.get("ma_long", 0)

    diff = ma_short - ma_long

    # =========================
    # RANGE（超緩和）
    # =========================
    if abs(diff) < 0.00001 and volatility < 0.00005:
        return {"action": "hold", "confidence": 0.0}

    # =========================
    # TREND判定（強制補正）
    # =========================
    if diff > 0:
        trend = "up"
    elif diff < 0:
        trend = "down"
    else:
        trend = "sideways"

    # =========================
    # VOLATILITY（ほぼ無効化）
    # =========================
    volatility_score = max(volatility, 0.00005)

    # =========================
    # ACTION（必ず出す構造）
    # =========================
    action = "buy" if trend == "up" else "sell"

    # =========================
    # CONFIDENCE（強制生成）
    # =========================
    confidence = min(0.95, abs(diff) * 3000 + volatility_score * 2000)

    # =========================
    # ANTI-SPAM（軽く）
    # =========================
    if StrategyState.last_action == action:
        StrategyState.same_count += 1
    else:
        StrategyState.same_count = 0
        StrategyState.last_action = action

    if StrategyState.same_count >= 10:
        return {"action": "hold", "confidence": 0.0}

    return {
        "action": action,
        "confidence": float(confidence)
    }