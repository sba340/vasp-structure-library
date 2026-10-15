"""Build an fcc(111) slab with ASE and write it as a VASP POSCAR file.

The slab uses an orthogonal surface cell, vacuum is added only above the
slab, and the bottom layers are frozen with selective dynamics.

Example (the Au(111) slab stored in this library):
    python generators/fcc111_slab.py --output structures/slabs/au-111-4x4x5/POSCAR
"""

import argparse

from ase import Atoms
from ase.build import fcc111
from ase.constraints import FixAtoms
from ase.io import write

AU_LATTICE_CONSTANT = 4.078  # Angstrom, FCC gold
BOTTOM_PAD = 0.5  # Angstrom, gap between lowest atoms and the cell floor


def build_slab(
    element="Au",
    lattice_constant=AU_LATTICE_CONSTANT,
    size=(4, 4, 5),
    vacuum=15.0,
    n_fixed_layers=2,
):
    """Return an fcc(111) slab with vacuum above and the bottom layers fixed.

    Parameters
    ----------
    element : str
        Chemical symbol of the metal.
    lattice_constant : float
        Bulk FCC lattice constant in Angstrom.
    size : tuple of int
        (nx, ny, n_layers) of the orthogonal surface cell.
    vacuum : float
        Vacuum thickness above the top layer in Angstrom.
    n_fixed_layers : int
        Number of layers, counted from the bottom, to freeze.
    """
    n_layers = size[2]
    if not 0 <= n_fixed_layers < n_layers:
        raise ValueError("n_fixed_layers must be >= 0 and smaller than the layer count.")

    # vacuum=None leaves the z-cell without padding; it is set manually below.
    slab = fcc111(element, size=size, a=lattice_constant, vacuum=None, orthogonal=True)

    # Shift the slab so the lowest layer sits just above the cell floor.
    z_min = slab.positions[:, 2].min()
    slab.translate((0.0, 0.0, BOTTOM_PAD - z_min))

    # Place vacuum only above the slab by resizing the z-axis of the cell.
    z_max = slab.positions[:, 2].max()
    cell = slab.cell.copy()
    cell[2, 2] = z_max + vacuum
    slab.set_cell(cell, scale_atoms=False)

    # ASE tags layers from the top (tag 1) to the bottom (tag n_layers).
    first_fixed_tag = n_layers - n_fixed_layers + 1
    slab.set_constraint(FixAtoms(mask=slab.get_tags() >= first_fixed_tag))
    return slab


def write_poscar(slab: Atoms, filename: str) -> None:
    """Write the slab in VASP5 format with direct (fractional) coordinates."""
    write(filename, slab, format="vasp", direct=True, vasp5=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--element", default="Au")
    parser.add_argument("--a", type=float, default=AU_LATTICE_CONSTANT,
                        help="lattice constant in Angstrom")
    parser.add_argument("--nx", type=int, default=4)
    parser.add_argument("--ny", type=int, default=4)
    parser.add_argument("--layers", type=int, default=5)
    parser.add_argument("--vacuum", type=float, default=15.0)
    parser.add_argument("--fixed-layers", type=int, default=2)
    parser.add_argument("--output", default="POSCAR")
    args = parser.parse_args()

    slab = build_slab(args.element, args.a, (args.nx, args.ny, args.layers),
                      args.vacuum, args.fixed_layers)
    write_poscar(slab, args.output)

    print(f"Number of atoms: {len(slab)}")
    print(f"Fixed atoms: {len(slab.constraints[0].index)}")
    print(f"Written to: {args.output}")


if __name__ == "__main__":
    main()
