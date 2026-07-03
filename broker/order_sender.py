import MetaTrader5 as mt5


class OrderSender:

    def send(self, order):

        symbol = order["symbol"]
        lot = order["lot"]
        order_type = order["type"]

        # -------------------------
        # HOLD
        # -------------------------
        if order_type == "HOLD":
            return {
                "success": True,
                "action": "hold",
                "ticket": None
            }

        # -------------------------
        # MT5準備
        # -------------------------
        if not mt5.symbol_select(symbol, True):
            return {
                "success": False,
                "error": "symbol_select_failed",
                "last_error": mt5.last_error()
            }

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return {
                "success": False,
                "error": "no_tick",
                "last_error": mt5.last_error()
            }

        # -------------------------
        # BUY / SELL 判定
        # -------------------------
        if order_type == "BUY":
            order_type_mt5 = mt5.ORDER_TYPE_BUY
            price = tick.ask
        elif order_type == "SELL":
            order_type_mt5 = mt5.ORDER_TYPE_SELL
            price = tick.bid
        else:
            return {
                "success": False,
                "error": "invalid_order_type"
            }

        # -------------------------
        # リクエスト作成
        # -------------------------
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot),
            "type": order_type_mt5,
            "price": price,
            "deviation": order.get("deviation", 20),
            "magic": order.get("magic", 10001),
            "comment": order.get("comment", "EA_SYSTEM"),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # -------------------------
        # 発注
        # -------------------------
        result = mt5.order_send(request)

        # -------------------------
        # 結果処理
        # -------------------------
        if result is None:
            return {
                "success": False,
                "error": "order_send_failed",
                "last_error": mt5.last_error()
            }

        return {
            "success": result.retcode == mt5.TRADE_RETCODE_DONE,
            "retcode": result.retcode,
            "ticket": result.order,
            "comment": result.comment
        }


