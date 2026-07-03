class PositionLimit:

    def __init__(self, max_positions=1):
        self.max_positions = max_positions

    def allow(self, current_positions):

        return current_positions < self.max_positions