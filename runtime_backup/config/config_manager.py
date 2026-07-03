import time
import importlib
import runtime.config.config as config


class ConfigManager:
    def __init__(self, reload_interval=5):
        self.reload_interval = reload_interval
        self.last_reload = 0
        self.config = config.CONFIG

    def get(self):
        return self.config

    def reload_if_needed(self):
        now = time.time()

        if now - self.last_reload >= self.reload_interval:
            try:
                # 設定ファイルを再読み込み
                importlib.reload(config)
                self.config = config.CONFIG
                self.last_reload = now
                print("[CONFIG] Reloaded")
            except Exception as e:
                print(f"[CONFIG ERROR] {e}")

        return self.config


