import MetaTrader5 as mt5
import time


class ConnectionManager:

    def __init__(self):
        self.connected = False

    def connect(self):

        if mt5.initialize():
            self.connected = True
            print("[MT5] connected")
            return True

        self.connected = False
        print("[MT5] connection failed")
        return False

    def check(self):

        # 接続チェック
        account = mt5.account_info()

        if account is None:
            self.connected = False
            return False

        return True

    def reconnect(self):

        print("[MT5] reconnecting...")

        mt5.shutdown()
        time.sleep(2)

        return self.connect()


