# ─────────────────────────────────────────────
#  SNIFFER SCREEN — sniffer.py
#  CAN frame capture and stats view.
#  Two modes: frame log (default) and
#  stats view (T to toggle).
# ─────────────────────────────────────────────

from textual.app        import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets    import Label

from ui.screens.base import BaseScreen


class SnifferScreen(BaseScreen):

    # False = frame log  |  True = stats view
    _stats_mode: bool = False
    _paused:     bool = False

    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("p",      "pause",          "Pause/Resume"),
        ("c",      "clear",          "Clear"),
        ("t",      "toggle_mode",    "Stats view"),
    ]

    # ── Layout ────────────────────────────────

    def screen_body(self) -> ComposeResult:
        with Horizontal(id="sniffer-toolbar"):
            yield Label("● RUNNING",     id="tb-state")
            yield Label("│",             classes="tb-sep")
            yield Label("frame log",     id="tb-mode")
            yield Label("│",             classes="tb-sep")
            yield Label("Frames: 0",     id="tb-count")
        with Vertical(id="sniffer-body"):
            yield Label("frame list goes here", id="sniffer-placeholder")

    # ── Actions ───────────────────────────────

    def action_pause(self) -> None:
        self._paused = not self._paused
        state_label  = self.query_one("#tb-state", Label)
        if self._paused:
            state_label.update("⏸  PAUSED")
            state_label.add_class("paused")
        else:
            state_label.update("● RUNNING")
            state_label.remove_class("paused")

    def action_clear(self) -> None:
        self.query_one("#tb-count", Label).update("Frames: 0")

    def action_toggle_mode(self) -> None:
        self._stats_mode = not self._stats_mode
        mode_label = self.query_one("#tb-mode", Label)
        if self._stats_mode:
            mode_label.update("stats view")
            mode_label.add_class("stats-active")
        else:
            mode_label.update("frame log")
            mode_label.remove_class("stats-active")