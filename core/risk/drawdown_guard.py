class DrawdownGuard:

    def __init__(self, max_dd=0.05):

        self.max_dd = max_dd
        self.peak_balance = 0
        self.current_balance = 0

    def update(self, balance):

        self.current_balance = balance

        if balance > self.peak_balance:
            self.peak_balance = balance

    def check(self):

        if self.peak_balance == 0:
            return True

        dd = (self.peak_balance - self.current_balance) / self.peak_balance

        if dd > self.max_dd:
            return False

        return True

    def get_dd(self):

        if self.peak_balance == 0:
            return 0

        return (self.peak_balance - self.current_balance) / self.peak_balance