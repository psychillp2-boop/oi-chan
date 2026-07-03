import time
import random
import logging
import threading


class LongRunTester:
    """
    24h Stability Test Runner

    Purpose:
    - Runtime stability check
    - Self-healing validation
    - MT5 reconnect stress test
    - Memory/loop survival test
    """

    def __init__(self, runtime, runtime_unit, duration_hours=24, interval=1.0):

        self.runtime = runtime
        self.unit = runtime_unit
        self.duration = duration_hours * 3600
        self.interval = interval

        self.running = False
        self.start_time = None

        # failure simulation flags
        self.inject_failure = True

    # -----------------------------
    # Fake load generator
    # -----------------------------
    def generate_state(self):
        return {
            "price": random.random(),
            "volume": random.randint(1, 100),
            "test_mode": True
        }

    # -----------------------------
    # optional chaos injection
    # -----------------------------
    def chaos(self, mt5):
        """
        ランダム障害（負荷テスト用）
        """
        if random.random() < 0.05:  # 5%確率
            try:
                print("[CHAOS] forcing MT5 shutdown")
                mt5.shutdown()
            except:
                pass

    # -----------------------------
    # main loop
    # -----------------------------
    def run(self):

        self.running = True
        self.start_time = time.time()

        logging.warning("=== 24H TEST START ===")

        while self.running:

            elapsed = time.time() - self.start_time

            # 終了条件
            if elapsed > self.duration:
                break

            try:
                state = self.generate_state()

                # ① Runtime cycle
                result = self.runtime.cycle(state)

                # ② TradingUnit cycle
                self.unit.run_cycle()

                # ③ Chaos injection
                if self.inject_failure:
                    self.chaos(self.runtime.broker)

                # ④ halt check
                if result.get("halt"):
                    logging.warning("[TEST] HALT triggered")

                # ⑤ log heartbeat
                if int(elapsed) % 60 == 0:
                    logging.info(f"[TEST] running {elapsed/60:.1f} min")

            except Exception as e:
                logging.error(f"[TEST ERROR] {e}")

            time.sleep(self.interval)

        self.running = False

        logging.warning("=== 24H TEST END ===")