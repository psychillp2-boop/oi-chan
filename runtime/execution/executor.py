import MetaTrader5 as mt5
import time


class Executor:

    def __init__(self):

        if not mt5.initialize():
            raise RuntimeError(f"MT5 INIT FAILED: {mt5.last_error()}")

        self.last_trade_time = 0

    # =========================
    # SL / TP
    # =========================
    def _calc_sl_tp(self, price, direction):

        pip = 0.01
        sl_pips = 200 * pip
        tp_pips = 200 * pip

        if direction == "BUY":
            sl = price - sl_pips
            tp = price + tp_pips
        else:
            sl = price + sl_pips
            tp = price - tp_pips

        return round(sl, 3), round(tp, 3)

    # =========================
    # LOG
    # =========================
    def _log_mt5(self, tag, result=None, error=None):
        print(f"[MT5][{tag}] RESULT:", result)
        if error:
            print(f"[MT5][ERROR]", error)

    # =========================
    # MAIN
    # =========================
    def execute(self, signal):

        now = time.time()

        # cooldown
        if now - self.last_trade_time < 2:
            return {"status": "skip", "reason": "COOLDOWN"}

        # HOLDはloop側で処理するのでここでは無視

        # BUY / SELLのみ処理
        if signal["type"] not in ["BUY", "SELL"]:
            return {"status": "error", "reason": "INVALID_SIGNAL"}

        symbol = "USDJPY"
        tick = mt5.symbol_info_tick(symbol)

        if not tick:
            return {"status": "error", "reason": "NO_TICK"}

        price = tick.ask if signal["type"] == "BUY" else tick.bid

        sl, tp = self._calc_sl_tp(price, signal["type"])

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": signal.get("lot", 0.01),
            "type": mt5.ORDER_TYPE_BUY if signal["type"] == "BUY" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "EA_EXEC",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        self._log_mt5("EXECUTED", result=result)
        self._log_mt5("LAST_ERROR", error=mt5.last_error())

        if result and result.retcode == mt5.TRADE_RETCODE_DONE:
            self.last_trade_time = now
            return {"status": "filled", "result": result._asdict()}

        return {
            "status": "rejected",
            "result": result._asdict() if result else None
        }