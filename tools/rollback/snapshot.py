import json
import time
from pathlib import Path
import shutil

SNAPSHOT_DIR = "tools/auditor/reports/snapshots"


def create_snapshot(plan):

    Path(SNAPSHOT_DIR).mkdir(parents=True, exist_ok=True)

    snapshot = {
        "time": time.time(),
        "moves": []
    }

    for m in plan["moves"]:

        snapshot["moves"].append({
            "src": m["src"],
            "dst": m["dst"]
        })

    path = f"{SNAPSHOT_DIR}/snapshot_{int(time.time())}.json"

    with open(path, "w") as f:
        json.dump(snapshot, f, indent=2)

    print("[SNAPSHOT CREATED]", path)

    return path