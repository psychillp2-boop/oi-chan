import MetaTrader5 as mt5


class Executor:

    def __init__(self, magic=10001):
        self.magic = magic

    # ==========================================
    # EXECUTE
    # ==========================================
    def execute(self, order):

        symbol = order["symbol"]

        if not mt5.initialize():
            return {
                "success": False,
                "error": "MT5_INIT_FAILED"
            }

        if not mt5.symbol_select(symbol, True):
            return {
                "success": False,
                "error": "SYMBOL_SELECT_FAILED"
            }

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return {
                "success": False,
                "error": "NO_TICK"
            }

        action = order["type"].lower()

        if action == "buy":
            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        elif action == "sell":
            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        else:
            return {
                "success": False,
                "error": "INVALID_ORDER_TYPE"
            }

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(order["lot"]),
            "type": order_type,
            "price": price,
            "sl": float(order.get("sl", 0.0)),
            "tp": float(order.get("tp", 0.0)),
            "deviation": 20,
            "magic": self.magic,
            "comment": "EA_SYSTEM",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result is None:
            return {
                "success": False,
                "error": "ORDER_SEND_FAILED"
            }

        return {
            "success": result.retcode == mt5.TRADE_RETCODE_DONE,
            "retcode": result.retcode,
            "order": getattr(result, "order", None),
            "deal": getattr(result, "deal", None),
            "price": price,
            "symbol": symbol,
            "volume": order["lot"],
            "type": action,
            "comment": getattr(result, "comment", "")
        }