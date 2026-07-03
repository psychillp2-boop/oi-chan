from pathlib import Path
from collections import defaultdict


ROOT = Path(__file__).resolve().parent.parent


def find_python_files():
    return list(ROOT.rglob("*.py"))


def count_folders():
    return [p for p in ROOT.rglob("*") if p.is_dir()]


def find_duplicate_names(py_files):
    groups = defaultdict(list)

    for f in py_files:
        groups[f.name].append(f)

    return {k: v for k, v in groups.items() if len(v) > 1}


def find_empty_folders():
    empty = []

    for d in ROOT.rglob("*"):
        if d.is_dir():
            try:
                if not any(d.iterdir()):
                    empty.append(d)
            except PermissionError:
                pass

    return empty


def print_header():
    print("=" * 50)
    print("EA_SYSTEM PROJECT AUDITOR v1")
    print("=" * 50)
    print()


def main():

    py_files = find_python_files()
    folders = count_folders()
    duplicates = find_duplicate_names(py_files)
    empty = find_empty_folders()

    print_header()

    print(f"Python files : {len(py_files)}")
    print(f"Folders      : {len(folders)}")
    print()

    print("Duplicate filenames")
    print("-" * 50)

    if duplicates:
        for name, files in sorted(duplicates.items()):
            print(f"\n{name}")
            for f in files:
                print("  ", f.relative_to(ROOT))
    else:
        print("None")

    print()
    print("Empty folders")
    print("-" * 50)

    if empty:
        for d in empty:
            print(d.relative_to(ROOT))
    else:
        print("None")

    print()
    print("Audit Complete.")


if __name__ == "__main__":
    main()