import time
import MetaTrader5 as mt5

from core.market.data_feed import get_market_data
from core.decision.strategy_router import get_signal
from runtime.execution.executor import Executor

SYMBOL = "USDJPY"

executor = Executor()

# =========================
# MT5 INIT
# =========================
if not mt5.initialize():
    print("[MT5] init failed")
    quit()

print("[MT5] Connected:", SYMBOL)


# =========================
# ポジション取得
# =========================
def get_position():
    positions = mt5.positions_get(symbol=SYMBOL)
    if positions:
        return positions[0]
    return None


# =========================
# 強制クローズ
# =========================
def close_position(pos):

    tick = mt5.symbol_info_tick(SYMBOL)

    if pos.type == 0:
        price = tick.bid
        order_type = mt5.ORDER_TYPE_SELL
    else:
        price = tick.ask
        order_type = mt5.ORDER_TYPE_BUY

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": pos.volume,
        "type": order_type,
        "position": pos.ticket,
        "price": price,
        "deviation": 20,
        "magic": pos.magic,
        "comment": "AUTO_CLOSE",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    mt5.order_send(request)


# =========================
# EXIT LOGIC（ここが重要）
# =========================
def should_close(pos):

    tick = mt5.symbol_info_tick(SYMBOL)

    profit = pos.profit

    # ① 利確
    if profit > 5:
        print("[EXIT] take profit")
        return True

    # ② 損切り
    if profit < -3:
        print("[EXIT] stop loss")
        return True

    # ③ 時間（簡易）
    if time.time() - pos.time > 60 * 30:
        print("[EXIT] time exit")
        return True

    return False


# =========================
# MAIN LOOP
# =========================
def run():

    print("🚀 EA START")

    while True:

        try:

            pos = get_position()

            # =========================
            # ポジション保有中
            # =========================
            if pos:

                print("[HOLD] position active")

                if should_close(pos):
                    close_position(pos)

                time.sleep(1)
                continue

            # =========================
            # エントリー処理
            # =========================
            market_data = get_market_data()
            signal = get_signal(market_data)

            if signal["action"] == "hold":
                time.sleep(1)
                continue

            result = executor.execute({
                "symbol": SYMBOL,
                "lot": 0.01,
                "type": signal["action"],
            })

            print("[ENTRY]", result)

            time.sleep(1)

        except Exception as e:
            print("[ERROR]", e)
            time.sleep(1)


if __name__ == "__main__":
    run()