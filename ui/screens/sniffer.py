# ─────────────────────────────────────────────
#  SNIFFER SCREEN — sniffer.py
#  CAN frame capture and stats view.
#  Two modes: frame log (default) and
#  stats view (T to toggle).
# ─────────────────────────────────────────────

from textual.app        import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets    import Label
from textual.widgets import Label, DataTable
from rich.text import Text

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
            yield Label("● RUNNING",    id="tb-state")
            yield Label("│",            classes="tb-sep")
            yield Label("frame log",    id="tb-mode")
            yield Label("│",            classes="tb-sep")
            yield Label("Frames: 0",    id="tb-count")
        yield DataTable(id="frame-table")
        with Horizontal(id="detail-panel"):
            with Vertical(classes="detail-cell"):
                yield Label("CAN ID",    classes="detail-label")
                yield Label("—",         id="detail-can-id")
            with Vertical(classes="detail-cell"):
                yield Label("Direction", classes="detail-label")
                yield Label("—",         id="detail-dir")
            with Vertical(classes="detail-cell"):
                yield Label("DLC",       classes="detail-label")
                yield Label("—",         id="detail-dlc")
            with Vertical(classes="detail-cell"):
                yield Label("Timestamp", classes="detail-label")
                yield Label("—",         id="detail-ts")
            with Vertical(classes="detail-cell"):
                yield Label("Decoded",   classes="detail-label")
                yield Label("—",         id="detail-decoded")
                

    def on_mount(self) -> None:
        self._frames = []       # stores raw frame tuples for detail panel
        self._frame_count = 0

        table = self.query_one(DataTable)
        table.add_column("Timestamp", width=14)
        table.add_column("CAN ID",    width=12)
        table.add_column("Dir",       width=5)
        table.add_column("DLC",       width=5)

        available     = self.size.width - 44
        data_width    = int(available * 0.55)
        decoded_width = int(available * 0.45)

        table.add_column("Data",    width=data_width)
        table.add_column("Decoded", width=decoded_width)

        table.cursor_type   = "row"
        table.zebra_stripes = True

        self._add_mock_data()


    # ── Helpers ───────────────────────────────
    def _add_mock_data(self) -> None:
        table  = self.query_one(DataTable)
        frames = [
            ("12:44:08.201", "0x7E4", "TX", "8", "02 22 D1 00 00 00 00 00", "ReadDID req 0xD100"),
            ("12:44:08.245", "0x7EC", "RX", "8", "04 62 D1 00 2F 42 00 00", "ReadDID resp 0xD100"),
            ("12:44:08.501", "0x7E4", "TX", "8", "02 22 D1 02 00 00 00 00", "ReadDID req 0xD102"),
            ("12:44:08.545", "0x7EC", "RX", "8", "04 62 D1 02 4E 27 00 00", "ReadDID resp 0xD102"),
            ("12:44:09.001", "0x7E4", "TX", "8", "02 3E 00 00 00 00 00 00", "TesterPresent"),
            ("12:44:09.055", "0x7EC", "RX", "8", "02 7E 00 00 00 00 00 00", "TesterPresent resp"),
            ("12:44:09.201", "0x7E4", "TX", "8", "02 22 D1 10 00 00 00 00", "ReadDID req 0xD110"),
            ("12:44:09.245", "0x7EC", "RX", "8", "04 62 D1 10 1A 2B 00 00", "ReadDID resp 0xD110"),
            ("12:44:09.501", "0x7E4", "TX", "8", "02 22 D1 20 00 00 00 00", "ReadDID req 0xD120"),
            ("12:44:09.545", "0x7EC", "RX", "8", "03 7F 22 31 00 00 00 00", "NRC 0x31 — requestOutOfRange"),
        ]
        for f in frames:
            self._frames.append(f)              # store raw tuple
            table.add_row(*self._make_row(*f))  # add colored row

        self.query_one("#tb-count", Label).update(f"Frames: {len(frames)}")
        
        
        
    def _make_row(self, ts: str, can_id: str, direction: str, dlc: str, data: str, decoded: str) -> tuple:
        """
        Returns a tuple of Rich Text objects with TX/RX coloring.
        TX rows — amber
        RX rows — teal
        """
        is_tx = direction.upper() == "TX"
        color  = "#ffb84d" if is_tx else "#00e5a0"     # amber / teal

        return (
            Text(ts,        style="#4a6080"),
            Text(can_id,    style="#4a6080"),
            Text(direction, style=f"bold {color}"),
            Text(dlc,       style="#4a6080"),
            Text(data,      style="#4a6080"),
            Text(decoded,   style="#4a6080"),
        )
        
        
    def on_data_table_row_highlighted( self, event: DataTable.RowHighlighted ) -> None:
        index = event.cursor_row      # current row index
        if index < 0 or index >= len(self._frames):
            return

        ts, can_id, direction, dlc, data, decoded = self._frames[index]

        # pick color based on direction
        color = "#ffb84d" if direction == "TX" else "#00e5a0"

        self.query_one("#detail-can-id",  Label).update(can_id)
        self.query_one("#detail-dir",     Label).update(direction)
        self.query_one("#detail-dlc",     Label).update(f"{dlc} bytes")
        self.query_one("#detail-ts",      Label).update(ts)
        self.query_one("#detail-decoded", Label).update(decoded)

        # color the direction label
        dir_label = self.query_one("#detail-dir", Label)
        dir_label.styles.color = color
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