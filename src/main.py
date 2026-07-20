import os
import sys
from pathlib import Path


def _fix_uv_python_tcl_tk() -> None:
    """uv-managed CPython builds on macOS bake in a build-time-only Tcl/Tk
    library path that doesn't exist at the actual install location, so
    tkinter fails to find init.tcl unless TCL_LIBRARY/TK_LIBRARY are pointed
    at the bundled copy explicitly. No-op wherever this isn't the case."""
    base = Path(sys.base_prefix)
    tcl_dir = base / "lib" / "tcl8.6"
    tk_dir = base / "lib" / "tk8.6"
    if tcl_dir.is_dir():
        os.environ.setdefault("TCL_LIBRARY", str(tcl_dir))
    if tk_dir.is_dir():
        os.environ.setdefault("TK_LIBRARY", str(tk_dir))


_fix_uv_python_tcl_tk()

import tkinter as tk  # noqa: E402 (must follow the Tcl/Tk env fix above)

from src.cat import Cat  # noqa: E402
from src.ui import GameWindow  # noqa: E402


def main() -> None:
    root = tk.Tk()
    cat = Cat(name="Whiskers")
    # Placeholder until Play (REQ-ACT-002) exists to deplete Energy
    # naturally — without this, Energy starts at its tested default of 10
    # (REQ-STAT-001) and there's nothing for Sleep to restore, so pressing
    # Sleep would loop sleeping.gif forever with no Waking Up transition.
    cat.energy.value = 5
    GameWindow(root, cat)
    root.mainloop()


if __name__ == "__main__":
    main()
