import MetaTrader5 as mt5


class Health:

    def check(self):

        if not mt5.initialize():
            return {"ok": False, "mt5": False}

        tick = mt5.symbol_info_tick("USDJPY")

        return {
            "ok": tick is not None,
            "mt5": True,
            "tick": tick is not None
        }