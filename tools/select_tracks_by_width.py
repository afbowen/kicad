# select_tracks_by_width.py
#
# Usage from KiCad Python console:
#
#   exec(open("/home/adam.bowen/git/kicad-projects/tools/select_tracks_by_width.py").read())
#   stw(0.127)
#
# Or, if KICAD_TOOLS is available:
#
#   import os
#   exec(open(os.path.join(os.environ["KICAD_TOOLS"], "select_tracks_by_width.py")).read())
#   stw(0.127)

import pcbnew


def stw(width_mm=0.127, clear_selection=True):
    """
    Select all PCB track segments with the specified width in mm.

    Example:
        stw(0.127)
        stw(0.2)
        stw(0.25)
    """

    board = pcbnew.GetBoard()
    target_width = pcbnew.FromMM(width_mm)

    if clear_selection:
        for item in board.GetTracks():
            item.ClearSelected()

    count = 0

    for item in board.GetTracks():
        # PCB_VIA inherits from PCB_TRACK, so explicitly exclude vias
        if isinstance(item, pcbnew.PCB_TRACK) and not isinstance(item, pcbnew.PCB_VIA):
            if item.GetWidth() == target_width:
                item.SetSelected()
                count += 1

    pcbnew.Refresh()
    print(f"Selected {count} track segment(s) with width {width_mm} mm")


# Slightly more descriptive alias
select_tracks_by_width = stw
