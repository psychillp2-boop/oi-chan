from pathlib import Path
from collections import defaultdict

def run(root="."):
    root_path = Path(root)

    files = defaultdict(list)

    for f in root_path.rglob("*.py"):
        files[f.name].append(str(f))

    duplicates = {k: v for k, v in files.items() if len(v) > 1}

    text = "[DUPLICATES]\n"
    for k, v in duplicates.items():
        text += f"\n{k}\n"
        for p in v:
            text += f"  {p}\n"

    return {
        "text": text,
        "raw": duplicates
    }