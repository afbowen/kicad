# KiCad Tools
These are tools for running in KiCad. These are generally run in the KiCad Python terminal.

## Environment Variables
These must exists in your `~/.profile` file in order to be accessible in the KiCad shell. You'll
need to log out and log back in after adding the lines in order for them to take effect.
```
export KICAD_PROJECTS=/home/adam.bowen/git/kicad-projects
export KICAD_TOOLS=$KICAD_PROJECTS/tools
```

## Tools

### Generate Sourcing Review from BOM
Point to a KiCad BOM and generate links to search each part in the BOM on the JLC PCB website to
find closest-match components that are in high supply. The workflow is...

1. Export a KiCad Schematic BOM
  - `Tools` → `Edit Symbol Fields...` → `Export`
  - Header should have these fields
    ```
    "Reference","Value","Critical","MPN","Class","Mfr","Voltage","Tolerance","JLCPCB_PN","Footprint","Dielectric_Class","Package","Description"
    ```
2. Run the `generate_sourcing_review.py` script pointing to the the BOM CSV
   ```
   python3 generate_sourcing_review.py path/to/input_bom.csv
   ```
3. Open the generated `sourcing_review.csv` using `gnumeric` (or other spreadsheet tool)
4. Use the generated JLC search URL to find a part with matching criteria specified in BOM
5. Find matching parts, add JLC part number to appropriate cell in CSV, update `Mfr` and `MPN`
   fields as needed

This basically just gets you an updated BOM CSV, which you'd use to manually update components (in
groups, not individually by instance) using the `Symbol Fields Table`. You could theoretically
write a script to look at the BOM with JLC updates vs. the one originally exported from KiCad and
highlight just the parts that require updates.


### Highlight Tracks of Width
Highlight all tracks/traces in a PCB layout of a specified width using `select_tracks_by_width.py`.
````.

# Once per session
import os
exec(open(os.path.join(os.environ["KICAD_TOOLS"], "select_tracks_by_width.py")).read())

# Subsequent runs to highlight (e.g.) 0.127mm tracks
stw(0.127)
```

OUTDATE
```
import os
WIDTH_MM = 0.127
exec(open(os.path.join(os.environ["KICAD_TOOLS"], "select_tracks_by_width.py")).read())
```
