def evaluate(metrics):

    trades = metrics.get("orders", 1)
    wins = metrics.get("wins", 0)

    winrate = wins / trades * 100 if trades > 0 else 0

    profit = metrics.get("profit", 0)
    dd = metrics.get("max_dd", 0)

    score = (profit * 2) + (winrate * 0.3) - (dd * 10)

    if score >= 90:
        verdict = "A+"
    elif score >= 75:
        verdict = "A"
    elif score >= 60:
        verdict = "B"
    else:
        verdict = "FAIL"

    return {
        "score": round(score, 2),
        "verdict": verdict,
        "winrate": winrate,
        "profit": profit,
        "dd": dd
    }