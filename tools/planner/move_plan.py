from pathlib import Path

def build_plan(target_path):

    print("=== BUILD PLAN ===")

    plan = {
        "moves": []
    }

    for file in Path(target_path).rglob("*.py"):
        plan["moves"].append({
            "src": str(file),
            "dst": str(file)  # 仮：ここは後で最適化
        })

    return plan