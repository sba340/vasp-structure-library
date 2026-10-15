"""Shared helpers for reading the structure library."""

import json
from pathlib import Path

from ase.io import read

ROOT = Path(__file__).resolve().parent.parent
STRUCTURES = ROOT / "structures"

REQUIRED_KEYS = ["name", "category", "description", "source_type", "date_added"]
SOURCE_TYPES = {"generated", "literature", "own-calculation", "database"}
REFERENCE_KEYS = ["authors", "title", "journal", "year", "doi"]


def find_entries():
    """Return a sorted list of directories that contain a metadata.json file."""
    return sorted(p.parent for p in STRUCTURES.rglob("metadata.json"))


def load_metadata(entry: Path) -> dict:
    with open(entry / "metadata.json", encoding="utf-8") as f:
        return json.load(f)


def load_atoms(entry: Path):
    return read(entry / "POSCAR", format="vasp")


def validate_entry(entry: Path):
    """Return a list of problems found in one structure folder."""
    problems = []
    if not (entry / "POSCAR").is_file():
        problems.append("missing POSCAR")
    meta = load_metadata(entry)

    for key in REQUIRED_KEYS:
        if not meta.get(key):
            problems.append(f"metadata missing '{key}'")

    source = meta.get("source_type")
    if source and source not in SOURCE_TYPES:
        problems.append(f"source_type must be one of {sorted(SOURCE_TYPES)}")

    if source in {"literature", "database"}:
        ref = meta.get("reference") or {}
        for key in REFERENCE_KEYS:
            if not ref.get(key):
                problems.append(f"literature entry needs reference.{key}")

    if (entry / "POSCAR").is_file():
        try:
            load_atoms(entry)
        except Exception as exc:  # unreadable POSCAR
            problems.append(f"POSCAR cannot be parsed: {exc}")
    return problems
