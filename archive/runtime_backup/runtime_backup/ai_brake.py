class AIBrake:

    def __init__(self):
        self.win = 0
        self.loss = 0
        self.recent_results = []

    def update(self, success: bool):

        self.recent_results.append(success)

        if success:
            self.win += 1
        else:
            self.loss += 1

        if len(self.recent_results) > 50:
            self.recent_results.pop(0)

    def should_stop(self):

        total = self.win + self.loss

        if total < 10:
            return False

        winrate = self.win / total

        # 勝率崩壊ライン
        if winrate < 0.45:
            return True

        # 直近連敗
        if self.recent_results[-5:] == [False]*5:
            return True

        return False

    def reset(self):
        self.win = 0
        self.loss = 0
        self.recent_results = []