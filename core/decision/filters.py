def apply_filters(state, data):

    # スプレッド緩和
    if data["spread"] > 5.0:
        return False, "spread_high"

    # セッション制限緩和
    if state["volatility"] == "HIGH" and state["session"] == "ASIA":
        return True, "override_volatility"

    return True, "ok"