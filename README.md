# vasp-structure-library

A curated collection of VASP `POSCAR` input structures and the scripts that
build them. The goal is to save time: structures that are tedious to build or
hard to find (surface slabs, doped oxides, published geometries) are stored
once, documented, and referenced.

Every structure has its own folder with a `POSCAR` and a `metadata.json`
that records what it is, how it was made, and where it came from.

See [CATALOG.md](CATALOG.md) for the full list.

## Layout

```
structures/      one folder per structure (POSCAR + metadata.json)
generators/      scripts that build structures with ASE
tools/           validation and catalog generation
templates/       metadata template for new entries
tests/           automated checks
```

## Quick start

```bash
git clone https://github.com/sba340/vasp-structure-library.git
cd vasp-structure-library
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Use a stored structure by copying its `POSCAR` into a VASP job directory.
Check `metadata.json` first for the functional, relaxation status, and notes.

Build a new fcc(111) slab:

```bash
python generators/fcc111_slab.py --element Cu --a 3.61 --layers 4 --output POSCAR
```

## Adding structures

Follow [ADDING_STRUCTURES.md](ADDING_STRUCTURES.md). Structures taken from
publications must include the full reference and DOI.

## Citing

If you use a structure that originates from a publication, cite the original
paper listed in its `metadata.json` and in `CATALOG.md`.


