# Adding a structure

1. Create a folder under `structures/<category>/<short-name>/`.
   Use lowercase names with hyphens, for example `structures/oxides/ito-bulk-80atoms/`.
2. Put the structure file in the folder and name it exactly `POSCAR`.
3. Copy `templates/metadata_template.json` into the folder, rename it `metadata.json`,
   and fill in every field.
4. For anything taken from a paper or database, fill in the full `reference`
   block (authors, title, journal, year, DOI) and the `permissions` field.
   Always give the credit, even when the file is in the supporting information.
5. Record anything that affects reuse in `calculation.notes`: whether the
   structure is relaxed, the functional, DFT+U values, magnetic ordering,
   dopant concentration and site positions, vacuum thickness, fixed layers.
6. Validate and rebuild the catalog:
   ```bash
   python tools/check_structures.py
   python tools/build_catalog.py
   ```
7. Commit the folder and the updated `CATALOG.md`.

## Rules for literature structures

- Do not alter the coordinates of a published structure. If you modify it
  (supercell, surface cut, relaxation), store it as a new entry and cite the
  original in `reference` and describe the change in `notes`.
- Check the journal or database license before sharing files that are not
  your own. Structures from supporting information are usually fine to share
  with citation, but confirm for each source.
- Keep the original POSCAR header comment line, or copy it into `notes`.
