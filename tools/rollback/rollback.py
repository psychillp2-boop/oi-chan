import json
import shutil
import os


def rollback(snapshot_path):

    print("=== ROLLBACK START ===")

    with open(snapshot_path, "r") as f:
        snapshot = json.load(f)

    # 逆順で戻す
    for m in reversed(snapshot["moves"]):

        src = m["src"]
        dst = m["dst"]

        try:
            if os.path.exists(dst):
                os.makedirs(os.path.dirname(src), exist_ok=True)

                shutil.move(dst, src)

                print(f"[RESTORED] {dst} → {src}")

        except Exception as e:
            print("[ROLLBACK ERROR]", e)

    print("=== ROLLBACK DONE ===")