exec_state = result.get("execution", {})

# =========================
# 🧠 EA LOG（判断専用）
# =========================
print(f"[EA][STATE] {exec_state.get('status')}")

if exec_state.get("blocked"):
    print(f"[EA][SAFETY] BLOCKED reason={exec_state.get('reason')}")

elif exec_state.get("status") == "filled":
    print("[EA][EXEC] SUCCESS")

elif exec_state.get("status") == "rejected":
    print(f"[EA][EXEC] REJECTED reason={exec_state.get('reason')}")

elif exec_state.get("status") == "error":
    print(f"[EA][EXEC] ERROR reason={exec_state.get('reason')}")