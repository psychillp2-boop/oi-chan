from pathlib import Path

def run(root="."):
    root_path = Path(root)

    python_files = list(root_path.rglob("*.py"))
    folders = [p for p in root_path.rglob("*") if p.is_dir()]

    return {
        "text": f"""
[SUMMARY]
Python files : {len(python_files)}
Folders      : {len(folders)}
""",
        "raw": {
            "python_files": len(python_files),
            "folders": len(folders)
        }
    }