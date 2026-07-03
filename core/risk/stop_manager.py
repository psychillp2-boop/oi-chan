# core/risk/stop_manager.py

from typing import Dict, Any


class StopManager:
    """
    Stop Manager

    Responsibility
    ----------------
    - Evaluate stop conditions
    - Return stop status only

    Never:
    - Send orders
    - Update StateStore
    - Access MT5 directly
    """

    def __init__(self, config=None):

        self.config = config or {}

        self.max_drawdown = self.config.get(
            "max_drawdown",
            0.20
        )

        self.max_daily_loss = self.config.get(
            "max_daily_loss",
            0.05
        )

        self.max_risk_score = self.config.get(
            "max_risk_score",
            0.70
        )

    # ---------------------------------
    # Stop Evaluation
    # ---------------------------------

    def evaluate(
        self,
        risk_score: float,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:

        drawdown = metrics.get(
            "drawdown",
            0.0
        )

        daily_loss = metrics.get(
            "daily_loss",
            0.0
        )

        if risk_score >= self.max_risk_score:

            return {
                "stop": True,
                "reason": "risk_score_limit"
            }

        if drawdown >= self.max_drawdown:

            return {
                "stop": True,
                "reason": "drawdown_limit"
            }

        if daily_loss >= self.max_daily_loss:

            return {
                "stop": True,
                "reason": "daily_loss_limit"
            }

        return {
            "stop": False,
            "reason": "ok"
        }