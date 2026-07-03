import time


class OrderThrottle:

    def __init__(self):

        self.last_time = {}

        self.cooldown = 5  # 秒

    def allow(self, ea_name):

        now = time.time()

        if ea_name not in self.last_time:
            self.last_time[ea_name] = 0

        if now - self.last_time[ea_name] < self.cooldown:
            return False

        self.last_time[ea_name] = now
        return True