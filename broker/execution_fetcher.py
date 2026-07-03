class ExecutionFetcher:
    def __init__(self, adapter):
        self.adapter = adapter

    def get_positions(self):
        return self.adapter.get_positions()

    def close(self, position_id):
        return self.adapter.close_order(position_id)


