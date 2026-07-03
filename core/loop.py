import time
import traceback
import MetaTrader5 as mt5

from core.market.data_feed import get_market_data
from core.decision.strategy_router import get_signal
from core.risk.risk_engine import evaluate_risk
from runtime.execution.executor import Executor

from core.risk.self_healing_engine import SelfHealingEngine
from core.risk.position_manager import PositionManager
from runtime.metrics_store import MetricsStore
from core.filters.filter_engine import FilterEngine


executor = Executor()
healing = SelfHealingEngine()
metrics = MetricsStore()
filter_engine = FilterEngine()

SYMBOL = "USDJPY"

pm = PositionManager(symbol=SYMBOL, max_positions=1, max_loss_pips=50)

last_trade_time = 0
cooldown_until = 0   # 🔥 追加（暴走防止）


def ensure_mt5():
    if mt5.initialize():
        return True
    mt5.shutdown()
    time.sleep(1)
    return mt5.initialize() or healing.recover_mt5()


if not ensure_mt5():
    quit()


def run_loop():

    global last_trade_time, cooldown_until

    print("[LOOP] START PRODUCTION MODE")

    while True:
        try:

            ensure_mt5()

            now = time.time()

            # =========================
            # 🔥 COOLDOWN制御（重要）
            # =========================
            if now < cooldown_until:
                time.sleep(1)
                continue

            rates = mt5.copy_rates_from_pos(SYMBOL, mt5.TIMEFRAME_M1, 0, 50)
            if rates is None:
                time.sleep(1)
                continue

            closes = [x[4] for x in rates]
            market_data = get_market_data(closes)

            signal = get_signal(market_data)

            signal_type = str(signal.get("action", "hold")).upper()
            confidence = float(signal.get("confidence", 0))

            print("[DEBUG SIGNAL]", signal_type, confidence)

            positions = mt5.positions_get(symbol=SYMBOL) or []

            print("[RAW POS]", len(positions))

            # =========================
            # FORCE CLOSE（安全版）
            # =========================
            if len(positions) >= pm.max_positions:

                print("[RECOVERY] FORCE CLOSE START")

                success_close = True

                for pos in positions:

                    tick = mt5.symbol_info_tick(SYMBOL)
                    if tick is None:
                        continue

                    close_request = {
                        "action": mt5.TRADE_ACTION_DEAL,
                        "symbol": SYMBOL,
                        "volume": pos.volume,
                        "position": pos.ticket,
                        "type": mt5.ORDER_TYPE_SELL if pos.type == 0 else mt5.ORDER_TYPE_BUY,
                        "price": tick.bid if pos.type == 0 else tick.ask,
                        "deviation": 20,
                        "magic": 123456,
                        "comment": "FORCE_CLOSE",
                        "type_filling": mt5.ORDER_FILLING_IOC
                    }

                    result = mt5.order_send(close_request)

                    print("[CLOSE RESULT]", result)

                    # 🔥 失敗検知
                    if result is None or result.retcode != 10009:
                        success_close = False

                # =========================
                # クールダウン制御
                # =========================
                if success_close:
                    print("[RECOVERY] CLOSE OK → cooldown 2s")
                    cooldown_until = now + 2
                else:
                    print("[RECOVERY] CLOSE FAILED → cooldown 5s")
                    cooldown_until = now + 5

                time.sleep(1)
                continue

            # =========================
            # FILTER
            # =========================
            if not filter_engine.allow(signal, confidence, now):
                print("[FILTER]", filter_engine.last_reason)
                time.sleep(1)
                continue

            # =========================
            # RISK
            # =========================
            if not evaluate_risk(signal, market_data):
                print("[RISK BLOCK]")
                time.sleep(1)
                continue

            # =========================
            # PRICE
            # =========================
            tick = mt5.symbol_info_tick(SYMBOL)
            symbol_info = mt5.symbol_info(SYMBOL)

            if tick is None:
                time.sleep(1)
                continue

            price = tick.ask if signal_type == "BUY" else tick.bid
            point = symbol_info.point

            order = {
                "type": signal_type,
                "lot": 0.01,
                "price": price,
                "sl": price - 50 * point if signal_type == "BUY" else price + 50 * point,
                "tp": price + 50 * point if signal_type == "BUY" else price - 50 * point,
            }

            result = executor.execute(order)

            # =========================
            # SUCCESS
            # =========================
            if result.get("status") == "filled":

                last_trade_time = now

                filter_engine.on_trade(signal_type, now)
                metrics.log_trade(result, market_data, signal)

                print("[TRADE]", result.get("result", {}).get("retcode"))
                print("[WINRATE]", metrics.win_rate())
                print("[PARAMS]", metrics.get_optimal_params())

                # 🔥 クールダウン（連打防止）
                cooldown_until = now + 1.5

            time.sleep(1)

        except Exception as e:
            print("[ERROR]", e)
            traceback.print_exc()
            time.sleep(1)


if __name__ == "__main__":
    run_loop()