class LossGuard:

    def __init__(self, max_loss_streak=3):
        self.max_loss_streak = max_loss_streak
        self.loss_streak = 0

    def update(self, result):

        if not result.get("success", False):
            self.loss_streak += 1
        else:
            self.loss_streak = 0

    def allow_trade(self):

        return self.loss_streak < self.max_loss_streak