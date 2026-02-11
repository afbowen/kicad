# KiCad Parts

## Overview
These are KiCad parts (symbols, footprints, 3D files) downloaded from the internet.


## Directory Structure

`symbols`
All schematic symbols of file tpye `.kicad_sym` go in here.

`footprints/Connectors.pretty`
All layout footprints of file type `.kicad_mod` for in here.

`3dmodels`
All 3D models (for 3D PCB rendering) of file type `.stp` go in here.

`zdownloads`
This directory does **not** contain references; it can be deleted at any time.

These are all the parts that were downloaded as packages. The relevant files from these packages
were copied into their appropriate homes in the `kicad_parts` directory. This directory can be
largely ignored, its just maintained for "why not?" reasons.


## Add a New Part

### Download Symbol, Footprint, 3D File
1. Find the part online (e.g. Mouser, UltraLibrarian) and download.
   - This should include...
     - A schematic symbol (`.kicad_sym`)
     - A schematic symbol (`.kicad_mod`)
     - A 3D part file (`.stp`)
2. Unzip the downloaded `.zip`.
3. If needed, create a new symbol library (see procedure below).
4. Add the downloaded symbol to the appropriate library (see procedure below).
5. Add the downloaded footprint to the appropriate library


### Symbol (schematic)
Symbols are objects in a library file.

#### Create a New Symbol Library
It generally makes sense to maintain a symbol library file for similar parts, instead of a symbol
file per part. For example, we can create a symbol library of connectors named `Custom_Connectors`
to which we can then add specific connector part symbols.

Note that the symbol library is itself a `.kicad_sym` file, **not** a directory.

1. Open KiCad
2. Open the Symbol Editor
3. Click `File -> New Library`
4. Select the **Global** Library Table
5. In the dialog box
   a. Select the directory where you're like to save the library
      (e.g. `~/.local/share/kicad/9.0/symbols`)
   b. Type a new library name of your choosing (e.g. `Custom_Connectors.kicad_sym`)
   c. Click the `Save` button.

_You should now see the library on the `Libraries` sidebar on the lefthand side of the Symbol
Editor window. Note that libraries are listed in alphabetical order, and you're should appear
accordingly in the list._

_You should also be able to go to the base KiCad window, select
`Preferences -> Manage Symbol Libraries`, and scroll to the bottom of the list to confirm it's been
created._

#### Add a Symbol
Add a downloaded symbol to an existing library.

1. Open KiCad
2. Open Symbol Editor
3. In the `Libraries` sidebar on the left, select the library (e.g. `Custom_Connectors`) to which
   you'd like to add the new symbol.
4. With the target library selected, import a new symbol by clicking into
   `File -> Import -> Symbol...`
5. Navigate to the downloaded `.kicad_sym` symbol file (e.g. `AT04-2P-BM02.kicad_sym`), select it,
   and click the `Open` button.
   - _The symbol should open in Symbol Editor, under the selected symbol library._
6. Save the symbol library with `Ctrl+S` or `File -> Save`


### Footprint (layout)
Footprints are files in a library folder.

#### Create a New Footprint Library
Different from symbols, the library is a directory that directly contains footprint files. Note
that the directory does have an extension -- `.pretty`.

1. Outside of KiCad, create the new directory that will serve as the footprint library; a `.pretty`
   extension is required in the name.
   ```
   # Example
   mkdir ~/.local/share/kicad/9.0/footprints/Custom_Connectors.pretty
   ```
2. Open KiCad
3. Select `Preferences -> Manage Footprint Libraries`
4. Click the button with the folder icon below the list and navigate to the `.pretty` folder
   created in Step 1.
5. Click the `OK` button.

_**NOTE**: this footprint will need to be explicitly linked to the corresponding symbol._

#### Add a Footprint
1. Outside of KiCad, simply copy the downloaded `.kicad_mod` file into the target footprint
   directory.


### 3D File (visualization)
Like footprints, 3D models are maintained under a directory. There's no library concept, and thus
no registration step. KiCad only knows about a 3D model if a footprint points to it.

1. Outside of KiCad, create the new directory that will serve as the 3D model library.
   ```
   # Example
   ~/.local/share/kicad/9.0/3dmodels/Custom_Connectors
   ```
2. Simply copy the downloaded `.stp` file into the target 3D model directory.

_**NOTE**: this 3D model will need to be explicitly linked to the corresponding footprint._

### Linking
Until now, the symbol, footprint, and 3D model have no relation. 3D models must be explicilty
pointed to by a footprint, and footprints must be linked to symbols.


#### Link a Footprint to a Symbol
1. Open KiCad
2. Open the Symbol Editor
3. In the `Libraries` sidebar on the left, expand the library (e.g. `Custom_Connectors`) and select
   the symbol to which you'd like to reference a footprint.
4. Open `Library Symbol Properties` for the selected symbol by pressing the `E` key.
   - If this opens the properties for a node, etc., click blank space around the symbol and try
     again.
5. Under `Fields`, find `Footprint` and specify the corresponding footprint in the format
   `<footprint_library>:<footprint_name>`.
   - e.g. `Custom_Connectors:AT042PMB02`
6. Click the `OK` button to exit the `Library Symbol Properties` dialog.
7. Save the updated footprint by clicking the save icon, or with `Ctrl+S`.

#### Link a 3D Moel to a Footprint
1. Open KiCad
2. Open the Footprint Editor
3. In the `Libraries` sidebar on the left, expand the library (e.g. `Custom_Connectors`) and select
   the footprint to which you'd like to add a 3D file.
4. Open `Footprint Properties` for the selected footprint by pressing the `E` key.
   - If this opens the properties for a pad, etc., click blank space around the footprint and try
     again.
5. In the dialog, select the `3D Models` tab.
6. On the `3D Models` tab, see under `3D Model(s)`, and select the folder icon button on the right.
7. In the file dialog, navigate to and select the target 3D model.
   - _This will load the 3D model, which should render in the `Footprint Properties` dialog._
8. Using the `Rotation` and `Offset` controls on the left, orient and position the part correctly
   to sit properly on the footprint.
9. Click the `OK` button to exit the `Footprint Properties` dialog.
10. Confirm the 3D model looks as it did in the `Footprint Properties` dialog by clicking
    `View -> 3D Viewer`.
10. Save the updated footprint by clicking the save icon, or with `Ctrl+S`.
