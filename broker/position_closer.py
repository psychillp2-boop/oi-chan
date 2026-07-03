import MetaTrader5 as mt5


def close_position(symbol, pos):

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"status": "error", "reason": "NO_TICK"}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": pos.volume,
        "position": pos.ticket,
        "type": mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY,
        "price": tick.bid if pos.type == 0 else tick.ask,
        "deviation": 20,
        "magic": 123456,
        "comment": "CLOSE",
    }

    result = mt5.order_send(request)

    if result is None:
        return {"status": "error", "reason": "FAILED"}

    return {"status": "closed", "result": result._asdict()}