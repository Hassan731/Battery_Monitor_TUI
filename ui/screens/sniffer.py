# ─────────────────────────────────────────────
#  SNIFFER SCREEN — sniffer.py
#  CAN frame capture and stats view.
#  Two modes: frame log (default) and
#  stats view (T to toggle).
# ─────────────────────────────────────────────

from textual.app    import ComposeResult
from textual.widgets import Label
from textual.containers import Horizontal, Vertical

from ui.screens.base import BaseScreen


class SnifferScreen(BaseScreen):

    # mode flag — False = frame log, True = stats view
    _stats_mode: bool = False

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("p",      "pause",          "Pause"),
        ("c",      "clear",          "Clear"),
        ("t",      "toggle_mode",    "Toggle mode"),
    ]

    def screen_body(self) -> ComposeResult:
        yield Label("CAN Sniffer — coming soon")

    def action_pause(self) -> None:
        pass   # placeholder

    def action_clear(self) -> None:
        pass   # placeholder

    def action_toggle_mode(self) -> None:
        self._stats_mode = not self._stats_mode
        mode = "stats" if self._stats_mode else "frame log"
        self.notify(f"Switched to {mode}")   # temporary feedback