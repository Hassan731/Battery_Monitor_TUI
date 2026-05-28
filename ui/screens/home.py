# ─────────────────────────────────────────────
#  HOME SCREEN — home.py
#  HomeScreen + FeatureCard widget
# ─────────────────────────────────────────────

from textual.app    import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Label
from textual.containers import Horizontal, Vertical
from textual.containers import Grid

from ui.screens.base import BaseScreen

from ui.screens.blackbox     import BlackBoxScreen
from ui.screens.live_monitor import LiveMonitorScreen
from ui.screens.did          import DIDScreen
from ui.screens.sniffer      import SnifferScreen
from ui.screens.routine      import RoutineScreen
from ui.screens.settings     import SettingsScreen


# ── Navigation map ────────────────────────────
#  Defines what happens when an arrow key is
#  pressed from each card index.
#
# grid layout:
# [0 BlackBox  ] [1 Sniffer  ]
# [2 LiveMon   ] [3 Routine  ]
# [4 DID r/w   ] [5 Settings ]

NAV = {
    #        right  down   left   up
    0: {"right": 1, "down": 2, "left": 0, "up": 0},
    1: {"right": 1, "down": 3, "left": 0, "up": 1},
    2: {"right": 3, "down": 4, "left": 2, "up": 0},
    3: {"right": 3, "down": 5, "left": 2, "up": 1},
    4: {"right": 5, "down": 4, "left": 4, "up": 2},
    5: {"right": 5, "down": 5, "left": 4, "up": 3},
}

# ── Screen map ────────────────────────────────
#  Maps each card index to its target screen.
#  Add new screens here as they are built.

SCREENS = {
    0: BlackBoxScreen,
    1: SnifferScreen,
    2: LiveMonitorScreen,
    3: RoutineScreen,
    4: DIDScreen,
    5: SettingsScreen,
}

# ── Feature card widget ───────────────────────
#  One card on the home screen.
#  Receives icon, label, and card_id from
#  HomeScreen. card_id is added as a CSS class
#  on mount so home.tcss can style each card
#  independently.

class FeatureCard(Widget):

    ALLOW_FOCUS = True          # allows keyboard focus
    can_focus = True          # required for mouse events to fire

    def __init__(self, icon: str, label: str, desc: str, card_id: str, index: int) -> None:
        super().__init__()
        self.icon    = icon
        self.label   = label
        self.desc    = desc
        self.card_id = card_id
        self._index = index

    def compose(self) -> ComposeResult:
        yield Label(self.icon,  classes="card-icon")
        with Vertical(classes="card-text"):
            yield Label(self.label, classes="card-name")
            yield Label(self.desc,  classes="card-desc")

    def on_mount(self) -> None:
        self.add_class(self.card_id)
        
    def on_click(self, event) -> None:
        # reuse the same action keyboard uses — keeps focus in sync
        self.screen.action_jump(self._index)
        self.screen.action_select() # click also opens the screen
        
    def on_mouse_enter(self, event) -> None:
        self.notify("hovered")
        self.add_class("hovered")

    def on_mouse_leave(self, event) -> None:
        self.remove_class("hovered")


# ── Home screen ───────────────────────────────
#  Entry point of the app. Displays all feature
#  cards in a two-column layout. Handles arrow
#  key navigation, number shortcuts, and Enter
#  to open the selected screen.

class HomeScreen(BaseScreen):

    BINDINGS = [
        # arrow navigation — shown in footer
        ("up",    "navigate('up')",    "Up"),
        ("down",  "navigate('down')",  "Down"),
        ("left",  "navigate('left')",  "Left"),
        ("right", "navigate('right')", "Right"),
        ("enter", "select",            "Open"),

        # number shortcuts — hidden from footer
        ("1", "jump(0)", ""),
        ("2", "jump(1)", ""),
        ("3", "jump(2)", ""),
        ("4", "jump(3)", ""),
        ("5", "jump(4)", ""),
        ("6", "jump(5)", ""),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._focus_index = 0   # card 0 (Black Box) is selected on launch

    # ── Layout ────────────────────────────────

    def screen_body(self) -> ComposeResult:
        with Grid(id="home-grid"):
            yield FeatureCard(icon="⏺", label="Black Box & Logging", desc="Record · export · replay",          card_id="card-bb"        , index=0)
            yield FeatureCard(icon="◉", label="CAN Sniffer",         desc="Live frame capture · filter",       card_id="card-sniff"     , index=1)
            yield FeatureCard(icon="⎍", label="Live Monitoring",     desc="Realtime DID polling",              card_id="card-live"      , index=2)
            yield FeatureCard(icon="▶", label="Routine Control",     desc="Trigger UDS routines",              card_id="card-routine"   , index=3)
            yield FeatureCard(icon="⊞", label="DID Read / Write",    desc="Read · write · decode bytes",       card_id="card-did"       , index=4)
            yield FeatureCard(icon="⚙", label="Settings",            desc="Bitrate · ECU address · timeouts",  card_id="card-set"       , index=5)
            
    def on_mount(self) -> None:
        # highlight the default card on startup
        self._get_card(self._focus_index).add_class("focused")

    # ── Helpers ───────────────────────────────

    def _get_card(self, index: int) -> FeatureCard:
        # returns the FeatureCard at the given index
        # order matches the compose() yield order
        return self.query(FeatureCard)[index]

    # ── Actions ───────────────────────────────

    def action_navigate(self, direction: str) -> None:
        # look up next index from NAV map and jump to it
        self.action_jump(NAV[self._focus_index][direction])

    def action_jump(self, index: int) -> None:
        # move focus from current card to target index
        self._get_card(self._focus_index).remove_class("focused")
        self._focus_index = index
        self._get_card(self._focus_index).add_class("focused")

    def action_select(self) -> None:
        # open the screen mapped to the currently focused card
        self.app.push_screen(SCREENS[self._focus_index]())