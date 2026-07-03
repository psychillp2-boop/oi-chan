import time

from core.market.data_feed import get_market_data
from core.decision.strategy_router import get_signal
from runtime.execution.executor import Executor

SYMBOL = "USDJPY"
executor = Executor(SYMBOL)

print("🚀 EA START")

while True:

    try:
        # ① market
        data = get_market_data()

        # ② decision
        signal = get_signal(data)

        # ③ execution
        if signal["action"] in ["BUY", "SELL"]:
            result = executor.execute({
                "type": signal["action"],
                "lot": 0.01
            })
            print("[EXEC]", result)

        else:
            print("[HOLD]")

        time.sleep(1)

    except Exception as e:
        print("[ERROR]", e)
        time.sleep(1)