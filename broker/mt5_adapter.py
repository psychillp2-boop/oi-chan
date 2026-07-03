import MetaTrader5 as mt5


class MT5Adapter:

    def __init__(self, client=None):
        self.client = client

        # MT5初期化
        if not mt5.initialize():
            raise RuntimeError("[MT5] initialize failed")

        account = mt5.account_info()
        if account is None:
            raise RuntimeError("[MT5] account_info failed")

        print("[MT5] connected")
        print("[MT5] balance:", account.balance)

    def execute(self, order):

        symbol = order["symbol"]
        volume = float(order["lot"])
        direction = order["type"]

        # シンボル有効化
        if not mt5.symbol_select(symbol, True):
            return {"success": False, "error": "SYMBOL_SELECT_FAILED"}

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return {"success": False, "error": "NO_TICK"}

        # 価格決定
        price = tick.ask if direction == "buy" else tick.bid

        # 注文タイプ
        if direction == "buy":
            order_type = mt5.ORDER_TYPE_BUY
        else:
            order_type = mt5.ORDER_TYPE_SELL

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "deviation": 20,
            "magic": 10001,
            "comment": "EA_SYSTEM",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        # エラーチェック
        if result is None:
            return {
                "success": False,
                "error": "ORDER_SEND_NONE"
            }

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {
                "success": False,
                "error": f"FAILED retcode={result.retcode}",
                "comment": result.comment
            }

        return {
            "success": True,
            "ticket": result.order,
            "price": price,
            "volume": volume,
            "symbol": symbol,
            "direction": direction,
            "message": "ORDER_EXECUTED"
        }

    def shutdown(self):
        """
        MT5接続を正常終了する
        """
        mt5.shutdown()
        print("[MT5] disconnected")