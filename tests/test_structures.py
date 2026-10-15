import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

from library import find_entries, validate_entry  # noqa: E402

from generators.fcc111_slab import build_slab  # noqa: E402


@pytest.mark.parametrize("entry", find_entries(), ids=lambda p: p.name)
def test_entry_is_valid(entry):
    assert validate_entry(entry) == []


def test_slab_generator_defaults():
    slab = build_slab()
    assert len(slab) == 80
    assert len(slab.constraints[0].index) == 32
