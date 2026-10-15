"""Check every structure folder for a readable POSCAR and complete metadata."""

import sys

from library import ROOT, find_entries, validate_entry


def main() -> int:
    failed = False
    for entry in find_entries():
        problems = validate_entry(entry)
        label = entry.relative_to(ROOT)
        if problems:
            failed = True
            print(f"FAIL {label}")
            for p in problems:
                print(f"     - {p}")
        else:
            print(f"ok   {label}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
