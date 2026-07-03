# runtime/monitor.py

import time


class Monitor:
    """
    System Monitor (SSOT)

    Responsibility:
    - Log collection
    - Error detection
    - Health check coordination
    """

    def __init__(self, logger, restart_handler=None):

        self.logger = logger
        self.restart_handler = restart_handler

        self.error_count = 0
        self.last_check = time.time()

    # -----------------------------
    # Log
    # -----------------------------

    def log(self, level, message):

        self.logger.write(level, message)

    # -----------------------------
    # Error tracking
    # -----------------------------

    def report_error(self, error):

        self.error_count += 1

        self.log("ERROR", str(error))

    # -----------------------------
    # Health check
    # -----------------------------

    def heartbeat(self):

        self.error_count = 0
        self.last_check = time.time()

    # -----------------------------
    # System status
    # -----------------------------

    def is_healthy(self):

        if self.error_count > 3:
            return False

        if time.time() - self.last_check > 60:
            return False

        return True

    # -----------------------------
    # Recovery hook
    # -----------------------------

    def try_recover(self):

        if self.restart_handler:
            return self.restart_handler.restart()

        return False