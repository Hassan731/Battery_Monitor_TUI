# ─────────────────────────────────────────────
#  STATUS BAR — status_bar.py
#  Displayed at the bottom of every screen.
#  Shows CAN connection, session, Tx/Rx counts.
# ─────────────────────────────────────────────

from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label


class StatusBar(Widget):

    def compose(self) -> ComposeResult:
        yield Label("● PCAN-USB", id="sb-connection")
        yield Label("│",          id="sb-sep1")
        yield Label("500 kbps",   id="sb-bitrate")
        yield Label("│",          id="sb-sep2")
        yield Label("Tx: 0",      id="sb-tx")
        yield Label("Rx: 0",      id="sb-rx")
        yield Label("│",          id="sb-sep3")
        yield Label("No session", id="sb-session")