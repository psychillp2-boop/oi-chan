# runtime/orchestrator.py

from runtime.trading_unit import TradingUnit


class Orchestrator:
    """
    Manage multiple EA TradingUnits
    """

    def __init__(self, store, engine, risk, safety, broker):

        self.store = store
        self.engine = engine
        self.risk = risk
        self.safety = safety
        self.broker = broker

        self.units = {}

    # -----------------------------
    # EA追加
    # -----------------------------

    def add_ea(self, ea_id):

        unit = TradingUnit(
            ea_id=ea_id,
            store=self.store,
            engine=self.engine,
            risk=self.risk,
            safety=self.safety,
            broker=self.broker
        )

        self.units[ea_id] = unit

    # -----------------------------
    # EA開始
    # -----------------------------

    def start(self, ea_id, interval=1.0):

        if ea_id not in self.units:
            raise ValueError(f"EA not found: {ea_id}")

        self.units[ea_id].run(interval)

    # -----------------------------
    # EA停止
    # -----------------------------

    def stop(self, ea_id):

        if ea_id in self.units:
            self.units[ea_id].stop()

    # -----------------------------
    # 全停止
    # -----------------------------

    def stop_all(self):

        for unit in self.units.values():
            unit.stop()