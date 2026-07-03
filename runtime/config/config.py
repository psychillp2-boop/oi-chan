# ==========================
# EA_SYSTEM CONFIG (ALL FIXED)
# ==========================

CONFIG = {

    # ==========================
    # ENV
    # ==========================
    "mode": "demo",          # demo / production
    "test_mode": True,

    # ==========================
    # SYMBOL
    # ==========================
    "symbol": "USDJPY",

    # ==========================
    # TRADE
    # ==========================
    "lot": 0.01,
    "max_positions": 1,
    "deviation": 20,

    # ==========================
    # RISK (重要)
    # ==========================
    "risk_limit": 0.02,      # 2%
    "sl_pips": 200,          # ★SL固定
    "tp_pips": 300,          # ★TP固定
    "max_drawdown": 0.05,

    # ==========================
    # EXECUTION CONTROL
    # ==========================
    "force_sl_tp": True,     # ★強制SL/TP
    "allow_trade": True,
    "cooldown_sec": 5,

    # ==========================
    # CONNECTION
    # ==========================
    "reconnect_interval": 5,

    # ==========================
    # TEST
    # ==========================
    "test_duration_sec": 60 * 30,
    "test_interval_sec": 5,

    # ==========================
    # LOG
    # ==========================
    "log_level": "INFO",
}