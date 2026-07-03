import MetaTrader5 as mt5


def close_all_positions():

    if not mt5.initialize():
        return {"status": "mt5_init_failed"}

    positions = mt5.positions_get()

    if positions is None or len(positions) == 0:
        return {"status": "no_positions"}

    results = []

    for pos in positions:

        symbol = pos.symbol
        volume = pos.volume

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            continue

        # BUYポジション → SELLで決済
        if pos.type == mt5.POSITION_TYPE_BUY:
            price = tick.bid
            order_type = mt5.ORDER_TYPE_SELL

        # SELLポジション → BUYで決済
        else:
            price = tick.ask
            order_type = mt5.ORDER_TYPE_BUY

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "position": pos.ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "CLOSE_ALL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        results.append({
            "ticket": pos.ticket,
            "retcode": result.retcode if result else None
        })

    return {
        "status": "closed",
        "results": results
    }


if __name__ == "__main__":
    print(close_all_positions())