from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widget import Widget
from textual.widgets import Header, Footer, Label


class FeatureCard(Widget):

    def __init__(self, icon: str, label: str, card_id: str) -> None:
        super().__init__()
        self.icon  = icon
        self.label = label
        self.card_id = card_id

    def compose(self) -> ComposeResult:
        yield Label(self.icon,  classes="card-icon")
        yield Label(self.label, classes="card-name")
        
    def on_mount(self) -> None:
        self.add_class(self.card_id)


class HomeScreen(Screen):

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="home-grid"):
            with Horizontal(id="col-main"):
                with Vertical(id="col-bb"):
                    yield FeatureCard(icon="📦", label="Black Box & Logging",  card_id="card-bb")
                with Vertical(id="col-mid"):
                    yield FeatureCard(icon="📡", label="Live Monitoring",       card_id="card-live")
                    yield FeatureCard(icon="📋", label="DID Read / Write",      card_id="card-did")
            with Vertical(id="col-right"):
                yield FeatureCard(icon="🔍", label="CAN Sniffer",           card_id="card-sniff")
                yield FeatureCard(icon="▶",  label="Routine Control",       card_id="card-routine")
                yield FeatureCard(icon="⚙",  label="Settings",              card_id="card-set")
        yield Footer()