from pathlib import Path
import ast

def run(root="."):
    root_path = Path(root)

    deps = {}

    for f in root_path.rglob("*.py"):
        try:
            tree = ast.parse(f.read_text(encoding="utf-8"))
        except:
            continue

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)

            if isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        deps[str(f)] = imports

    return {
        "text": "[DEPENDENCIES READY]",
        "raw": deps
    }