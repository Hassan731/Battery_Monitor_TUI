# ─────────────────────────────────────────────
#  HOME SCREEN — home.py
#  HomeScreen + FeatureCard widget
# ─────────────────────────────────────────────

from textual.app    import ComposeResult
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Label
from textual.containers import Horizontal, Vertical

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
#  Layout reference:
#  [0 BlackBox] [1 LiveMon ] [3 Sniffer ]
#               [2 DID r/w ] [4 Routine ]
#                            [5 Settings]

NAV = {
    #        right  down   left   up
    0: {"right": 1, "down": 1, "left": 0, "up": 0},
    1: {"right": 3, "down": 2, "left": 0, "up": 1},
    2: {"right": 4, "down": 2, "left": 0, "up": 1},
    3: {"right": 3, "down": 4, "left": 1, "up": 3},
    4: {"right": 4, "down": 5, "left": 2, "up": 3},
    5: {"right": 5, "down": 5, "left": 2, "up": 4},
}


# ── Screen map ────────────────────────────────
#  Maps each card index to its target screen.
#  Add new screens here as they are built.

SCREENS = {
    0: BlackBoxScreen,
    1: LiveMonitorScreen,
    2: DIDScreen,
    3: SnifferScreen,
    4: RoutineScreen,
    5: SettingsScreen,
}


# ── Feature card widget ───────────────────────
#  One card on the home screen.
#  Receives icon, label, and card_id from
#  HomeScreen. card_id is added as a CSS class
#  on mount so home.tcss can style each card
#  independently.

class FeatureCard(Widget):

    def __init__(self, icon: str, label: str, card_id: str) -> None:
        super().__init__()
        self.icon    = icon
        self.label   = label
        self.card_id = card_id

    def compose(self) -> ComposeResult:
        yield Label(self.icon,  classes="card-icon")
        yield Label(self.label, classes="card-name")

    def on_mount(self) -> None:
        self.add_class(self.card_id)


# ── Home screen ───────────────────────────────
#  Entry point of the app. Displays all feature
#  cards in a two-column layout. Handles arrow
#  key navigation, number shortcuts, and Enter
#  to open the selected screen.

class HomeScreen(Screen):

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

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="home-grid"):
            with Horizontal(id="col-main"):
                with Vertical(id="col-bb"):
                    yield FeatureCard(icon="📦", label="Black Box & Logging", card_id="card-bb")
                with Vertical(id="col-mid"):
                    yield FeatureCard(icon="📡", label="Live Monitoring",     card_id="card-live")
                    yield FeatureCard(icon="📋", label="DID Read / Write",    card_id="card-did")
            with Vertical(id="col-right"):
                yield FeatureCard(icon="🔍", label="CAN Sniffer",         card_id="card-sniff")
                yield FeatureCard(icon="▶",  label="Routine Control",     card_id="card-routine")
                yield FeatureCard(icon="⚙",  label="Settings",            card_id="card-set")
        yield Footer()

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