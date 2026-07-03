# runtime/trading_unit.py

import time

from runtime.runtime import Runtime


class TradingUnit:
    """
    Trading Unit

    Responsibility
    ----------------
    - Manage one EA instance
    - Execute Runtime cycle
    - Update StateStore
    - Handle start / stop

    Never:
    - Implement strategy
    - Calculate risk
    - Communicate with MT5 directly
    """

    def __init__(
        self,
        ea_id,
        store,
        engine,
        risk,
        safety,
        broker
    ):

        self.ea_id = ea_id
        self.store = store

        self.runtime = Runtime(
            store=store,
            engine=engine,
            risk=risk,
            safety=safety,
            broker=broker
        )

        self.running = False

    # ---------------------------------
    # Start
    # ---------------------------------

    def run(self, interval=1.0):

        self.running = True

        while self.running:

            # 1. Read SSOT
            state = self.store.get_state()

            # 2. Runtime Cycle
            result = self.runtime.cycle(state)

            # 3. Update Decision
            self.store.update(
                "decision",
                result["decision"]
            )

            # 4. Update Risk
            self.store.update(
                "risk",
                result["risk"]
            )

            # 5. Update Execution
            if result["execution"] is not None:

                self.store.update(
                    "execution",
                    result["execution"]
                )

            # 6. Safety Halt
            if result["halt"]:

                self.store.set_halt(
                    f"{self.ea_id}_halted"
                )

            # 7. Wait
            time.sleep(interval)

    # ---------------------------------
    # Stop
    # ---------------------------------

    def stop(self):

        self.running = False