from .rules import is_protected

def dry_run(plan: dict):

    out = []
    out.append("\n[DRY RUN MOVE EXECUTION]\n")

    for file, data in plan.items():

        out.append(file)
        out.append(f"  KEEP: {data['keep']}")

        for m in data["moves"]:

            if is_protected(m):
                out.append(f"  BLOCKED: {m}")
                continue

            out.append(f"  WOULD MOVE: {m} → _archive")

        out.append("")

    return "\n".join(out)