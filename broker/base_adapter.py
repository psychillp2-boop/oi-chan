class BaseAdapter:
    def send_order(self, signal):
        raise NotImplementedError

    def close_order(self, position_id):
        raise NotImplementedError

    def get_positions(self):
        raise NotImplementedError


