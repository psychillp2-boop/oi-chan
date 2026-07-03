import MetaTrader5 as mt5


class PositionManager:

    def __init__(self, symbol, max_positions=1, max_loss_pips=50):
        self.symbol = symbol
        self.max_positions = max_positions
        self.max_loss_pips = max_loss_pips
        self.last_block_reason = None

    # =========================
    # エントリー制御
    # =========================
    def allow_entry(self):

        positions = mt5.positions_get(symbol=self.symbol) or []

        if len(positions) >= self.max_positions:
            self.last_block_reason = "MAX_POSITIONS"
            return False

        return True

    # =========================
    # 強制クローズ（重要修正）
    # =========================
    def force_close(self):

        positions = mt5.positions_get(symbol=self.symbol) or []

        for pos in positions:

            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                continue

            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": self.symbol,
                "volume": pos.volume,
                "position": pos.ticket,
                "type": mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY,
                "price": tick.bid if pos.type == 0 else tick.ask,
                "deviation": 20,
                "magic": 123456,
                "comment": "FORCE_CLOSE",
            }

            result = mt5.order_send(close_request)

            # 🔥 成功確認
            if result is None or result.retcode != 10009:
                self.last_block_reason = f"CLOSE_FAILED:{result.retcode if result else 'NONE'}"
                return False

        return True

    # =========================
    # 損失監視（軽量）
    # =========================
    def loss_guard(self):

        positions = mt5.positions_get(symbol=self.symbol) or []

        for pos in positions:

            tick = mt5.symbol_info_tick(self.symbol)
            if tick is None:
                continue

            price = tick.bid if pos.type == 0 else tick.ask
            loss_pips = abs(price - pos.price_open)

            if loss_pips > self.max_loss_pips * 0.0001:
                self.last_block_reason = "LOSS_LIMIT"
                return False

        return True