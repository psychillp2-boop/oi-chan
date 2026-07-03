import MetaTrader5 as mt5


class PositionGuard:

    def __init__(self, symbol):
        self.symbol = symbol

    def has_position(self):
        positions = mt5.positions_get(symbol=self.symbol)
        return positions is not None and len(positions) > 0

    def get_positions(self):
        return mt5.positions_get(symbol=self.symbol) or []

    def opposite_position(self, signal_type):
        positions = self.get_positions()

        for pos in positions:
            pos_type = "BUY" if pos.type == 0 else "SELL"

            if pos_type != signal_type:
                return pos

        return None