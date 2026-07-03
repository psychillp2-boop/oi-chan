PRIORITY_MAP = {
    "core/": 0,
    "runtime/": 1,
    "tools/": 2,
    "core_backup/": 3,
    "_archive": 4,
}

PROTECTED_PATTERNS = [
    "main.py",
    "engine.py",
    "risk_engine.py",
]

def get_priority(path: str) -> int:
    for k, v in PRIORITY_MAP.items():
        if k in path:
            return v
    return 999


def is_protected(path: str) -> bool:
    return any(p in path for p in PROTECTED_PATTERNS)