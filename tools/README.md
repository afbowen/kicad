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

### Highlight Tracks of Width
Highlight all tracks/traces in a layout of a specified width using `

```
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
